# HỒ SƠ ĐỒ ÁN MÔN HỌC CS315 - MÁY HỌC NÂNG CAO
## ĐỀ TÀI: DỰ BÁO SỰ LAN TRUYỀN SÓNG ÙN TẮC TRÊN ĐỒ THỊ GIAO THÔNG ĐÔ THỊ TP.HCM KẾT HỢP DỮ LIỆU THỜI TIẾT ĐA PHƯƠNG THỨC VÀ KHAI THÁC ĐỒ THỊ TRI THỨC HỖ TRỢ CẢNH BÁO LỘ TRÌNH

[![UIT](https://img.shields.io/badge/UIT-ĐHQG--HCM-blue.svg)](https://www.uit.edu.vn/)
[![Course](https://img.shields.io/badge/Course-CS315.G12.LT.TTNT-1F4E79.svg)](#)
[![Progress](https://img.shields.io/badge/Progress-0%25%20(Fast--track%20Kickoff)-orange.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![ML-Frameworks](https://img.shields.io/badge/Frameworks-Scikit--Learn%20%7C%20LightGBM%20%7C%20XGBoost%20%7C%20PyTorch-green.svg)](#)
[![XAI](https://img.shields.io/badge/Explainability-SHAP%20TreeExplainer-red.svg)](#)
[![KG](https://img.shields.io/badge/Knowledge%20Graph-NetworkX%20%7C%20GraphRAG-purple.svg)](#)

---

* **Đơn vị đào tạo:** Khoa Khoa học Máy tính / Hệ thống Thông tin – Trường Đại học Công nghệ Thông tin (ĐHQG-HCM)
* **Giảng viên hướng dẫn:** ThS. Đặng Việt Dũng
* **Học phần:** `CS315.G12.LT.TTNT` (Máy học nâng cao) – Học kỳ 1, Năm học 2026 – 2027
* **Mô hình triển khai:** Tự chủ hoàn toàn trong nội bộ `CS315` (thu thập – làm sạch – chọn lọc đặc trưng – mô hình hóa – giải thích XAI – Knowledge Graph khép kín bằng Python/Colab)
* **Kế hoạch tiến độ:** Fast-track Sprint 6 tuần (Tuần 3 – Tuần 8), **Hoàn tất & Nghiệm thu tại Tuần 8 (15/12/2026)**.

---

### DANH SÁCH NHÓM 5 THÀNH VIÊN & PHÂN CÔNG CHUYÊN TRÁCH

| STT | Họ và Tên | MSSV | Vai Trò Chuyên Trách | Đầu Việc Chính Trong Dự Án (Fast-track) |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Trần Hoàng Hôn** | `26410046` | **Trưởng nhóm / PM & Đồ thị giao thông** | Quản trị tiến độ WBS, trích xuất đồ thị OSMnx cụm Ngã tư Hàng Xanh (Nodes, Edges, Ma trận kề), chuẩn hóa bài toán và điều phối báo cáo tổng thể |
| 2 | **Nguyễn Duy Khang** | `26410055` | **Kỹ sư Dữ liệu & Feature Selection** | Chuẩn hóa 2 nhánh dữ liệu sạch (tập cảm biến thực tế `METR-LA` đối chứng & bộ Hàng Xanh: `OSMnx`, `Open-Meteo`, lịch triều Phú An, giao thông mô phỏng tăng cường); thực thi pipeline Feature Selection (Variance Threshold, Pearson r, One-Hot, Chi2, nhánh đối chứng PCA) bám sát Buổi 2 |
| 3 | **Phạm Thành Trung** | `26410141` | **Kỹ sư AI & Mô hình hóa học máy** | Huấn luyện Baseline ML (Random Forest, LightGBM, XGBoost) & ST-GNN; tối ưu hàm loss phạt class_weight='balanced' hướng tới Recall >= 85% cho pha kẹt nặng |
| 4 | **Vũ Văn Duy** | `26410031` | **Kỹ sư Giải thích XAI & GIS Heatmap** | Khởi tạo khung GIS (Folium) kiểm tra tọa độ nút thực địa từ Tuần 4; phân tích SHAP values bóc tách biến mưa/ngập; dựng bản đồ nhiệt trực quan hóa sóng ùn tắc |
| 5 | **Hoàng Cao Sơn** | `25730061` | **Kỹ sư Đồ thị tri thức & AI Agent** | Khảo sát nghiên cứu quốc tế từ Tuần 4 (luồng song song độc lập); thiết kế Schema Traffic Knowledge Graph & phát triển module AI Agent hỏi - đáp lộ trình |

---

### CẤU TRÚC HỒ SƠ ĐỒ ÁN TRONG THƯ MỤC

```text
├── 📄 De_Cuong_Chi_Tiet_Do_An_May_Hoc_Nang_Cao.docx  <-- [BẢN IN/NỘP THẦY] Đề cương chi tiết (Word chuẩn CITD/UIT)
├── 📊 Ke_Hoach_Thuc_Hien_Do_An_May_Hoc_Nang_Cao.xlsx  <-- [BẢN KẾ HOẠCH NỘP] Tiến độ 6 tuần SV/GV đánh giá (Excel)
├── 📝 De_Cuong_Chi_Tiet_Do_An_May_Hoc_Nang_Cao.md    <-- Bản thuyết minh Markdown 7 mục nội dung đầy đủ
├── 📋 DS_Nhom_CS315.G12.LT.TTNT.xlsx               <-- Dòng đăng ký chuẩn đề tài trên file chung của lớp
└── 📖 README.md                                    <-- Bản hướng dẫn & tổng quan hồ sơ đồ án (File này)
```

---

### SƠ ĐỒ KIẾN TRÚC GIẢI PHÁP (TỰ CHỦ TRONG CS315)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ TẦNG THU THẬP & TIỀN XỬ LÝ DỮ LIỆU (PYTHON / PANDAS - ĐỘC LẬP TRONG CS315)  │
│ • Nhánh 1 (Benchmark thật): Tập cảm biến giao thông chuẩn mở METR-LA        │
│ • Nhánh 2 (Kịch bản TP.HCM): Đồ thị OSMnx (Hàng Xanh 15–25 nút)             │
│   + Open-Meteo (mưa/ẩm/nhiệt) + Lịch triều Phú An + Lưu lượng mô phỏng      │
│   ──► Pandas Clean / Imputation / Time Alignment (UTC+7, bước 15 phút)      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (Dữ liệu bảng sạch chuẩn hóa)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ TẦNG ĐẶC TRƯNG & ĐỒ THỊ (FEATURE ENGINEERING & SELECTION)                   │
│ 1. Trích xuất mạng lưới đường Hàng Xanh (OSMnx: Nodes, Edges, Ma trận kề)   │
│ 2. Feature Selection: Variance Threshold / Pearson r ➔ One-Hot + Chi2 (>5.99)│
│    (Nhánh PCA tách riêng để đối chứng, giữ tên gốc cho SHAP TreeExplainer)  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ TẦNG MÔ HÌNH HỌC MÁY & TỐI ƯU HÓA (MACHINE LEARNING CORE)                   │
│ • Baseline Models: Random Forest, LightGBM, XGBoost                         │
│ • Nâng cao: Spatial-Temporal GNN (Đồ thị không gian - thời gian)            │
│ • Hàm Loss & Độ đo: Tối ưu Recall >= 85% & F1 >= 80% (Pha ùn tắc nặng)     │
│ • Dự báo lan truyền theo thời gian: t + 15' | t + 30' | t + 60'             │
└───────────────────┬─────────────────────────────────────┬───────────────────┘
                    │                                     │
                    ▼                                     ▼
┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
│ TẦNG GIẢI THÍCH MÔ HÌNH (XAI)        │  │ TẦNG ĐỒ THỊ TRI THỨC (GRAPH RAG) │
│ • SHAP Values (TreeExplainer)        │  │ • Traffic Knowledge Graph         │
│ • Đánh giá tác động lượng mưa/ngập   │  │   (Nút - Tuyến kề - Điểm ngập)    │
│ • Xóa bỏ tính hộp đen (Black-box)    │  │ • AI Agent tra cứu lộ trình né    │
└───────────────────┬──────────────────┘  └───────────────────┬───────────────┘
                    │                                         │
                    └───────────────────┬─────────────────────┘
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ TẦNG TRỰC QUAN HÓA & NGHIỆM THU (DELIVERABLES TUẦN 8)                       │
│ 1. Bản đồ nhiệt GIS trực quan hóa động thái lan truyền sóng ùn tắc (Folium) │
│ 2. Module AI Agent tương tác tự nhiên hỏi - đáp lộ trình                    │
│ 3. Báo cáo hoàn chỉnh 40–50 trang + Slide 25–30 trang + Video Clip Demo     │
│ 4. Nghiệm thu hoàn tất 100% đồ án môn học với ThS. Đặng Việt Dũng          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### BẢNG TIẾN ĐỘ THỰC HIỆN CHI TIẾT (RÚT GỌN ĐẾN HẾT TUẦN 8)

| Tuần | Thời Gian | Nội Dung Công Việc (Fast-track Sprint) | Phụ Trách | Tiến Độ |
| :---: | :---: | :--- | :--- | :---: |
| **Tuần 3** | 04/11 – 10/11 | Khởi tạo đề tài, viết Thuyết minh Đề cương chi tiết (MD), Kế hoạch thực hiện (XLSX) & chuẩn hóa dòng đăng ký file lớp. | Trần Hoàng Hôn (Lead) & Cả nhóm | **0%** |
| **Tuần 4** | 11/11 – 17/11 | Trích xuất đồ thị OSMnx cụm Hàng Xanh; dựng khung GIS (Folium) kiểm tra tọa độ thực địa; mock pipeline ML & hàm đo Recall; khảo sát quốc tế & Schema Traffic KG; xin Thầy Dũng góp ý 13/11. | Hôn, Khang, Trung, Duy, Sơn | **0%** |
| **Tuần 5** | 18/11 – 24/11 | Hoàn thiện 2 nhánh dữ liệu sạch (`METR-LA` đối chứng & Hàng Xanh: `OSMnx` + `Open-Meteo` + lịch triều Phú An + mô phỏng tăng cường); dứt điểm Feature Selection (Variance, Pearson, One-Hot, Chi2, nhánh PCA); huấn luyện Baseline ML (RF, LightGBM, XGBoost) dự báo sau 15'-30'-60'; dựng Traffic KG mẫu. | Khang, Trung, Sơn, Duy | **0%** |
| **Tuần 6** | 25/11 – 01/12 | Nâng cấp mô hình đồ thị/Ensemble tối ưu Recall $\ge 85\%$ & F1-Score; áp dụng SHAP values bóc tách biến mưa ngập; thử nghiệm AI Agent gọi tool tra cứu lộ trình. | Trung, Duy, Sơn, Hôn | **0%** |
| **Tuần 7** | 02/12 – 08/12 | Xây dựng bản đồ nhiệt trực quan hóa lan truyền sóng (Folium); hoàn thiện AI Agent; hoàn thành 100% nội dung Báo cáo Word/PDF (40–50 trang); đóng gói GitHub repo. | Duy, Sơn, Hôn, Trung, Khang | **0%** |
| **Tuần 8** | 09/12 – 15/12 | Thiết kế Slide thuyết trình (25–30 slide); quay video clip demo kịch bản sóng ùn tắc khi mưa; BÁO CÁO VÀ NGHIỆM THU ĐỒ ÁN VỚI THẦY DŨNG; nộp trọn bộ hồ sơ. | Cả nhóm 5 thành viên (Hôn điều phối) | **0%** |

*(Ghi chú: Toàn bộ đồ án kết thúc và nghiệm thu hoàn tất vào cuối Tuần 8. Các tuần 9–11 dành trọn vẹn cho việc ôn thi cuối kỳ các học phần khác).*

---

### CÔNG NGHỆ & MÔI TRƯỜNG PHÁT TRIỂN

* **Ngôn ngữ:** Python 3.10+
* **Xử lý đồ thị & Không gian:** OSMnx, NetworkX, GeoPandas, Shapely, Folium
* **Lựa chọn đặc trưng:** Scikit-learn (`VarianceThreshold`, `SelectKBest`, `chi2`, `PCA`), SciPy (`pearsonr`)
* **Mô hình học máy:** Scikit-learn (Random Forest), LightGBM, XGBoost, PyTorch Geometric (GCN/GAT/ST-GNN)
* **Giải thích mô hình (XAI):** SHAP (`TreeExplainer`, `SummaryPlot`, `ForcePlot`)
* **AI Agent & Đồ thị tri thức:** LangChain / LlamaIndex / Agentic Tool-calling
* **Quản trị phiên bản:** Git & GitHub (`mrkiss-it/cs315-traffic-congestion-graph-ml`)
