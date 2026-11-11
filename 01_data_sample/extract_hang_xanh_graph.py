"""Trích xuất và chuẩn hóa đồ thị mạng lưới đường cụm Ngã tư Hàng Xanh (CS315 - [H3]).

Quy trình:
1. Tải đồ thị đường lái xe (`network_type='drive'`, `simplify=True`) trong bán kính 1000 m quanh Ngã tư Hàng Xanh bằng OSMnx kèm bộ lọc đường trục chính (`custom_filter`).
2. Lọc nhánh theo 6 trục đường giới hạn của đề cương (loại bỏ đường hẻm nội khu), giữ các cầu/nút vòng xoay liên thông nội tại.
3. Chiếu sang hệ tọa độ mét (UTM), gộp các nút gần nhau tại vòng xoay/nút giao lớn (`consolidate_intersections`) và hợp nhất cặp làn đối chiều phân cách trên đại lộ.
4. Rút gọn các nút chia đoạn ngắn trên cùng một tuyến đường, loại bỏ cạnh song song trùng hướng, gán `node_id` (`HX_01`..`HX_N`) theo khoảng cách từ tâm Hàng Xanh.
5. Xuất `nodes.csv`, `edges.csv`, `adjacency_matrix.csv` và `hang_xanh.graphml` trong `01_data_sample/`.
"""

from __future__ import annotations

import argparse
import math
import pathlib
import tempfile
import time
from typing import Any

import networkx as nx
import osmnx as ox
import pandas as pd
from shapely.geometry import Point

DEFAULT_CENTER = (10.8012, 106.7114)
DEFAULT_DIST_M = 1000
MAJOR_ROADS_FILTER = (
    '["highway"~"trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link"]'
)

TARGET_AXIS_KEYWORDS = (
    "Xô Viết Nghệ Tĩnh",
    "Đinh Bộ Lĩnh",
    "Bạch Đằng",
    "Điện Biên Phủ",
    "Nguyễn Gia Trí",
    "Ung Văn Khiêm",
    "Hàng Xanh",
    "Cầu Đinh Bộ Lĩnh",
    "Cầu Sơn",
    "Cầu Văn Thánh",
)

HIGHWAY_PRIORITY = {
    "trunk": 0,
    "trunk_link": 1,
    "primary": 2,
    "primary_link": 3,
    "secondary": 4,
    "secondary_link": 5,
    "tertiary": 6,
    "tertiary_link": 7,
}

OVERPASS_MIRRORS = (
    "https://overpass-api.de/api",
    "https://overpass.kumi.systems/api",
)


def _flatten_values(val: Any) -> list[str]:
    """Chuẩn hóa thuộc tính OSM (có thể là scalar, list lồng nhau hoặc None) thành danh sách chuỗi."""
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return []
    if isinstance(val, (list, tuple, set)):
        out: list[str] = []
        for item in val:
            out.extend(_flatten_values(item))
        return out
    return [str(val).strip()]


def _unique_ordered(items: list[str]) -> list[str]:
    seen: set[str] = set()
    res: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            res.append(item)
    return res


def matches_target_axes(name_val: Any) -> bool:
    """Kiểm tra cạnh có thuộc 6 trục đường mục tiêu quanh Hàng Xanh hay không (loại trừ Hẻm)."""
    vals = _flatten_values(name_val)
    if not vals:
        return False
    joined = " | ".join(vals)
    if "hẻm" in joined.lower():
        return False
    lowered = joined.lower()
    return any(kw.lower() in lowered for kw in TARGET_AXIS_KEYWORDS)


def fetch_raw_graph(
    center: tuple[float, float] = DEFAULT_CENTER,
    dist_m: int = DEFAULT_DIST_M,
    cache_dir: pathlib.Path | None = None,
) -> nx.MultiDiGraph:
    """Tải đồ thị OSMnx quanh Hàng Xanh với bộ nhớ đệm ngoài repo và cơ chế thử lại qua mirror."""
    ox.settings.use_cache = True
    ox.settings.cache_folder = cache_dir or (pathlib.Path(tempfile.gettempdir()) / "osmnx_cache")

    last_err: Exception | None = None
    for mirror in OVERPASS_MIRRORS:
        ox.settings.overpass_url = mirror
        for attempt in range(2):
            try:
                return ox.graph_from_point(
                    center,
                    dist=dist_m,
                    network_type="drive",
                    simplify=True,
                    custom_filter=MAJOR_ROADS_FILTER,
                )
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                time.sleep(2 * (attempt + 1))

    raise RuntimeError(f"Không thể tải dữ liệu Overpass qua các mirror: {last_err}") from last_err


def filter_target_axes(G: nx.MultiDiGraph) -> nx.MultiDiGraph:
    """Giữ các cạnh thuộc 6 trục đường Hàng Xanh và các đoạn nối ngắn nội tại không tên."""
    axis_edges = [
        (u, v, k)
        for u, v, k, data in G.edges(keys=True, data=True)
        if matches_target_axes(data.get("name"))
    ]
    G_axes = G.edge_subgraph(axis_edges).copy()
    axis_nodes = set(G_axes.nodes())

    sub_edges = [
        (u, v, k)
        for u, v, k, data in G.edges(keys=True, data=True)
        if u in axis_nodes
        and v in axis_nodes
        and (not _flatten_values(data.get("name")) or matches_target_axes(data.get("name")))
    ]
    G_sub = G.edge_subgraph(sub_edges).copy()
    if G_sub.number_of_nodes() == 0:
        raise ValueError("Đồ thị sau lọc 6 trục đường rỗng.")

    # Chỉ giữ thành phần liên thông yếu lớn nhất để đảm bảo không còn nút cô lập
    largest_wcc = max(nx.weakly_connected_components(G_sub), key=len)
    return G_sub.subgraph(largest_wcc).copy()


def merge_close_nodes(G_utm: nx.MultiDiGraph, max_dist_m: float = 65.0) -> nx.MultiDiGraph:
    """Gộp các nút quá gần (chủ yếu là 2 chiều đường phân cách hoặc nhánh biên) trên mặt phẳng UTM."""
    nodes = sorted(G_utm.nodes())
    proximity = nx.Graph()
    proximity.add_nodes_from(nodes)
    for idx, u in enumerate(nodes):
        ux, uy = G_utm.nodes[u]["x"], G_utm.nodes[u]["y"]
        for v in nodes[idx + 1 :]:
            vx, vy = G_utm.nodes[v]["x"], G_utm.nodes[v]["y"]
            if math.hypot(ux - vx, uy - vy) <= max_dist_m:
                proximity.add_edge(u, v)

    merged = nx.MultiDiGraph()
    merged.graph.update(G_utm.graph)
    node_map: dict[Any, int] = {}

    for new_id, comp in enumerate(sorted(nx.connected_components(proximity), key=lambda c: min(c))):
        comp_list = sorted(comp)
        merged.add_node(
            new_id,
            x=sum(G_utm.nodes[n]["x"] for n in comp_list) / len(comp_list),
            y=sum(G_utm.nodes[n]["y"] for n in comp_list) / len(comp_list),
        )
        for old_n in comp_list:
            node_map[old_n] = new_id

    for u, v, _, data in G_utm.edges(keys=True, data=True):
        nu, nv = node_map[u], node_map[v]
        if nu == nv:
            continue
        nd = dict(data)
        nd.pop("geometry", None)
        merged.add_edge(nu, nv, **nd)

    return merged


def contract_short_splits(G_utm: nx.MultiDiGraph, max_combined_len: float = 450.0) -> nx.MultiDiGraph:
    """Rút gọn nút trung gian bậc-2 trên cùng một tuyến đường nếu chiều dài gộp <= max_combined_len."""
    H = G_utm.copy()
    changed = True
    while changed:
        changed = False
        for node in sorted(list(H.nodes())):
            nbrs = (set(H.predecessors(node)) | set(H.successors(node))) - {node}
            if len(nbrs) != 2:
                continue

            inc = list(H.in_edges(node, data=True))
            out = list(H.out_edges(node, data=True))
            if not inc or not out:
                continue

            roads: set[str] = set()
            for _, _, d in inc + out:
                roads.update(_flatten_values(d.get("name")))
            if len(roads) > 1:
                continue

            candidate_pairs = [
                (u, v, d1, d2) for u, _, d1 in inc for _, v, d2 in out if u != v
            ]
            if not candidate_pairs:
                continue
            max_len = max(
                float(d1.get("length", 0.0)) + float(d2.get("length", 0.0))
                for _, _, d1, d2 in candidate_pairs
            )
            if max_len > max_combined_len:
                continue

            H.remove_node(node)
            for u, v, d1, d2 in candidate_pairs:
                nd = dict(d1)
                nd["length"] = float(d1.get("length", 0.0)) + float(d2.get("length", 0.0))
                nd.pop("geometry", None)
                H.add_edge(u, v, **nd)
            changed = True
            break
    return H


def _pick_highway(edges_data: list[dict[str, Any]]) -> str:
    raw = _unique_ordered([h for d in edges_data for h in _flatten_values(d.get("highway"))])
    if not raw:
        return "unclassified"
    return min(raw, key=lambda h: (HIGHWAY_PRIORITY.get(h, 99), h))


def _pick_lanes(edges_data: list[dict[str, Any]]) -> int:
    parsed: list[int] = []
    for d in edges_data:
        for token in _flatten_values(d.get("lanes")):
            try:
                parsed.append(int(float(token)))
            except ValueError:
                continue
    return max(parsed) if parsed else 2


def _pick_maxspeed(edges_data: list[dict[str, Any]]) -> int | None:
    parsed: list[int] = []
    for d in edges_data:
        for token in _flatten_values(d.get("maxspeed")):
            digits = "".join(ch for ch in token if ch.isdigit())
            if digits:
                parsed.append(int(digits))
    return max(parsed) if parsed else None


def dedup_and_normalize_edges(G_utm: nx.MultiDiGraph) -> nx.MultiDiGraph:
    """Hợp nhất các cạnh song song cùng cặp nút (u -> v) và chuẩn hóa kiểu vô hướng/scalar."""
    clean = nx.MultiDiGraph()
    clean.graph.update(G_utm.graph)
    for n, d in G_utm.nodes(data=True):
        clean.add_node(n, **d)

    grouped: dict[tuple[Any, Any], list[dict[str, Any]]] = {}
    for u, v, _, d in G_utm.edges(keys=True, data=True):
        grouped.setdefault((u, v), []).append(d)

    for (u, v), ds in sorted(grouped.items()):
        names = _unique_ordered([n for d in ds for n in _flatten_values(d.get("name"))])
        road_name = " / ".join(names) if names else "Đoạn nối Hàng Xanh"
        highway = _pick_highway(ds)
        lanes = _pick_lanes(ds)
        maxspeed = _pick_maxspeed(ds)
        avg_length = round(sum(float(d.get("length", 0.0)) for d in ds) / len(ds), 2)
        oneway = all(bool(d.get("oneway", False)) for d in ds)

        attrs: dict[str, Any] = {
            "name": road_name,
            "highway": highway,
            "lanes": lanes,
            "length": avg_length,
            "oneway": oneway,
        }
        if maxspeed is not None:
            attrs["maxspeed"] = maxspeed
        clean.add_edge(u, v, **attrs)

    return clean


def relabel_by_center_distance(
    G_utm: nx.MultiDiGraph,
    center: tuple[float, float] = DEFAULT_CENTER,
) -> tuple[nx.MultiDiGraph, pd.DataFrame]:
    """Đặt lại node_id dạng HX_01..HX_N theo khoảng cách từ tâm Hàng Xanh và dựng bảng nút."""
    G_ll = ox.project_graph(G_utm, to_crs="EPSG:4326")

    # Chiếu điểm tâm Hàng Xanh sang UTM để đo khoảng cách chính xác bằng mét
    center_geom, _ = ox.projection.project_geometry(
        Point(center[1], center[0]),
        crs="EPSG:4326",
        to_crs=G_utm.graph["crs"],
    )
    cx, cy = center_geom.x, center_geom.y

    ranked = sorted(
        G_utm.nodes(),
        key=lambda n: (
            math.hypot(G_utm.nodes[n]["x"] - cx, G_utm.nodes[n]["y"] - cy),
            -G_ll.nodes[n]["y"],
            G_ll.nodes[n]["x"],
        ),
    )
    id_map = {old_n: idx for idx, old_n in enumerate(ranked, start=1)}

    G_final = nx.MultiDiGraph()
    G_final.graph["crs"] = "EPSG:4326"
    G_final.graph["name"] = "Hang_Xanh_Key_Corridors"

    node_rows: list[dict[str, Any]] = []
    for old_n in ranked:
        nid = id_map[old_n]
        node_code = f"HX_{nid:02d}"
        lat = round(float(G_ll.nodes[old_n]["y"]), 6)
        lon = round(float(G_ll.nodes[old_n]["x"]), 6)
        utm_x = round(float(G_utm.nodes[old_n]["x"]), 2)
        utm_y = round(float(G_utm.nodes[old_n]["y"]), 2)
        dist_center_m = round(math.hypot(utm_x - cx, utm_y - cy), 1)

        inc_edges = list(G_utm.in_edges(old_n, data=True))
        out_edges = list(G_utm.out_edges(old_n, data=True))
        roads = _unique_ordered(
            [nm for _, _, d in inc_edges + out_edges for nm in _flatten_values(d.get("name")) if nm != "Đoạn nối Hàng Xanh"]
        )
        hw_classes = _unique_ordered(
            [str(d.get("highway")) for _, _, d in inc_edges + out_edges if d.get("highway")]
        )

        G_final.add_node(
            nid,
            x=lon,
            y=lat,
            lat=lat,
            lon=lon,
            node_code=node_code,
            roads=" | ".join(roads),
            dist_center_m=dist_center_m,
        )
        node_rows.append(
            {
                "node_id": nid,
                "node_code": node_code,
                "lat": lat,
                "lon": lon,
                "roads": " | ".join(roads),
                "highway_classes": " | ".join(hw_classes),
                "in_degree": len(inc_edges),
                "out_degree": len(out_edges),
                "dist_center_m": dist_center_m,
                "utm_x": utm_x,
                "utm_y": utm_y,
            }
        )

    for u, v, _, d in sorted(G_utm.edges(keys=True, data=True), key=lambda e: (id_map[e[0]], id_map[e[1]])):
        nu, nv = id_map[u], id_map[v]
        G_final.add_edge(nu, nv, **d)

    return G_final, pd.DataFrame(node_rows)


def build_hang_xanh_graph(
    center: tuple[float, float] = DEFAULT_CENTER,
    dist_m: int = DEFAULT_DIST_M,
    consolidation_tolerance_m: float = 30.0,
    merge_dist_m: float = 65.0,
    max_contract_len_m: float = 450.0,
    cache_dir: pathlib.Path | None = None,
    from_graphml: pathlib.Path | None = None,
) -> tuple[nx.MultiDiGraph, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Pipeline hoàn chỉnh tạo đồ thị 15–25 nút cụm Hàng Xanh kèm bảng nút, cạnh và ma trận kề."""
    if from_graphml is not None:
        G_raw = ox.load_graphml(from_graphml)
    else:
        G_raw = fetch_raw_graph(center=center, dist_m=dist_m, cache_dir=cache_dir)

    G_sub = filter_target_axes(G_raw)
    G_utm = ox.project_graph(G_sub)
    G_cons = ox.consolidate_intersections(
        G_utm,
        rebuild_graph=True,
        tolerance=consolidation_tolerance_m,
        dead_ends=False,
    )
    G_merged = merge_close_nodes(G_cons, max_dist_m=merge_dist_m)
    G_contracted = contract_short_splits(G_merged, max_combined_len=max_contract_len_m)
    G_clean = dedup_and_normalize_edges(G_contracted)
    G_final, nodes_df = relabel_by_center_distance(G_clean, center=center)

    edge_set = {(u, v) for u, v in G_final.edges()}
    edge_rows: list[dict[str, Any]] = []
    for idx, (u, v, d) in enumerate(
        sorted(G_final.edges(data=True), key=lambda e: (e[0], e[1])),
        start=1,
    ):
        edge_rows.append(
            {
                "edge_id": f"E_{idx:02d}",
                "u": u,
                "v": v,
                "name": d["name"],
                "highway": d["highway"],
                "lanes": d["lanes"],
                "length": d["length"],
                "oneway": d["oneway"],
                "bidirectional_pair": (v, u) in edge_set,
                "maxspeed": d.get("maxspeed", ""),
            }
        )
    edges_df = pd.DataFrame(edge_rows)

    node_order = nodes_df["node_id"].tolist()
    adj_df = nx.to_pandas_adjacency(G_final, nodelist=node_order, weight=None, dtype=int)

    return G_final, nodes_df, edges_df, adj_df


def export_graph_artifacts(
    output_dir: pathlib.Path,
    G_final: nx.MultiDiGraph,
    nodes_df: pd.DataFrame,
    edges_df: pd.DataFrame,
    adj_df: pd.DataFrame,
) -> dict[str, pathlib.Path]:
    """Lưu nodes.csv, edges.csv, adjacency_matrix.csv và hang_xanh.graphml với kiểm tra nhất quán."""
    output_dir.mkdir(parents=True, exist_ok=True)
    n_nodes = len(nodes_df)
    if not (15 <= n_nodes <= 25):
        raise ValueError(f"Số nút sau rút gọn ({n_nodes}) nằm ngoài khoảng mục tiêu 15–25.")
    if nx.number_weakly_connected_components(G_final) != 1:
        raise ValueError("Đồ thị xuất ra chưa liên thông yếu thành 1 thành phần.")
    if adj_df.shape != (n_nodes, n_nodes):
        raise ValueError(f"Kích thước ma trận kề {adj_df.shape} không khớp {n_nodes} nút.")
    if int(adj_df.values.sum()) != len(edges_df):
        raise ValueError("Tổng cạnh ma trận kề không khớp số dòng edges.csv.")

    paths = {
        "nodes": output_dir / "nodes.csv",
        "edges": output_dir / "edges.csv",
        "adjacency": output_dir / "adjacency_matrix.csv",
        "graphml": output_dir / "hang_xanh.graphml",
    }
    nodes_df.to_csv(paths["nodes"], index=False, encoding="utf-8-sig")
    edges_df.to_csv(paths["edges"], index=False, encoding="utf-8-sig")
    adj_df.to_csv(paths["adjacency"], encoding="utf-8-sig")
    ox.save_graphml(G_final, filepath=paths["graphml"])
    return paths


def parse_args() -> argparse.Namespace:
    default_out = pathlib.Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Trích xuất đồ thị đường cụm Hàng Xanh (CS315 - [H3]).")
    parser.add_argument("--center-lat", type=float, default=DEFAULT_CENTER[0])
    parser.add_argument("--center-lon", type=float, default=DEFAULT_CENTER[1])
    parser.add_argument("--dist", type=int, default=DEFAULT_DIST_M)
    parser.add_argument("--tolerance", type=float, default=30.0)
    parser.add_argument("--merge-dist", type=float, default=65.0)
    parser.add_argument("--max-contract-len", type=float, default=450.0)
    parser.add_argument("--output-dir", type=pathlib.Path, default=default_out)
    parser.add_argument("--from-graphml", type=pathlib.Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    G_final, nodes_df, edges_df, adj_df = build_hang_xanh_graph(
        center=(args.center_lat, args.center_lon),
        dist_m=args.dist,
        consolidation_tolerance_m=args.tolerance,
        merge_dist_m=args.merge_dist,
        max_contract_len_m=args.max_contract_len,
        from_graphml=args.from_graphml,
    )
    paths = export_graph_artifacts(args.output_dir, G_final, nodes_df, edges_df, adj_df)
    print(f"Extracted Hang Xanh graph: {len(nodes_df)} nodes, {len(edges_df)} directed edges")
    for key, path in paths.items():
        print(f"  - {key}: {path}")


if __name__ == "__main__":
    main()

