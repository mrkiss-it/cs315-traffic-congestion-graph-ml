# ĐỀ CƯƠNG CHI TIẾT ĐỒ ÁN MÔN HỌC CS315
## MÔN: MÁY HỌC NÂNG CAO (ADVANCED MACHINE LEARNING)
### HỌC KỲ 1 – NĂM HỌC 2026 – 2027

---

**ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH**  
**TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN**  
**KHOA HỆ THỐNG THÔNG TIN / TRÍ TUỆ NHÂN TẠO**

---

### THÔNG TIN CHUNG

* **TÊN ĐỀ TÀI (Tiếng Việt):**  
  **Nghiên cứu mô hình học máy dự báo sự lan truyền sóng ùn tắc trên đồ thị giao thông đô thị TP.HCM kết hợp dữ liệu thời tiết đa phương thức và khai thác đồ thị tri thức hỗ trợ cảnh báo lộ trình**
* **TÊN ĐỀ TÀI (Tiếng Anh):**  
  *Research on Machine Learning Models for Traffic Congestion Wave Propagation Prediction on Ho Chi Minh City Urban Road Graph Integrated with Multi-modal Weather Data and Knowledge Graph for Route Alerting*
* **Cán bộ hướng dẫn (CBHD):** ThS. Đặng Việt Dũng
* **Mã lớp học phần:** `CS315.G12.LT.TTNT`
* **Thời gian thực hiện:** Từ ngày 23/10/2026 đến cuối tháng 12/2026 (Theo khung đào tạo HK1 2026–2027)
* **Sinh viên thực hiện (Nhóm 5 thành viên):**

| STT | Họ và Tên Sinh Viên | Mã Số Sinh Viên | Lớp Sinh Hoạt | Vai Trò Đảm Trách Trong Đồ Án |
| :---: | :--- | :---: | :---: | :--- |
| 1 | **Trần Hoàng Hôn** | `26410046` | AI2026 | **Trưởng nhóm / Project Manager & Đồ thị giao thông:** Quản trị tiến độ, điều phối kỹ thuật, trích xuất cấu trúc đồ thị mạng lưới đường OSMnx khu vực Hàng Xanh, chuẩn hóa bài toán và hoàn thiện báo cáo tổng hợp. |
| 2 | **Nguyễn Duy Khang** | `26410055` | AI2026 | **Kỹ sư Dữ liệu & Lựa chọn đặc trưng (Feature Selection):** Xây dựng pipeline thu thập & làm sạch 2 nhánh dữ liệu (`METR-LA` đối chứng & Hàng Xanh: `OSMnx`, thời tiết `Open-Meteo`, lịch triều Phú An, giao thông mô phỏng tăng cường), triển khai lọc đặc trưng (Pearson $r$, Variance Threshold, One-Hot, $\chi^2$, nhánh đối chứng PCA) và quản trị bộ dữ liệu thực nghiệm. |
| 3 | **Phạm Thành Trung** | `26410141` | AI2026 | **Kỹ sư AI / Mô hình hóa Machine Learning:** Thiết kế và huấn luyện các mô hình dự báo lan truyền sóng ùn tắc (Baseline ML: Random Forest, LightGBM/XGBoost vs. mô hình đồ thị), thẩm định độ đo rủi ro (`Recall`, `F1-Score`, `TimeSeriesSplit`). |
| 4 | **Vũ Văn Duy** | `26410031` | AI2026 | **Kỹ sư Giải thích mô hình (XAI) & Trực quan hóa:** Phân tích mức độ đóng góp đặc trưng bằng SHAP values / Feature Importance (khắc phục tính hộp đen), xây dựng bản đồ nhiệt trực quan hóa sự lan truyền sóng ùn tắc. |
| 5 | **Hoàng Cao Sơn** | `25730061` | AI2026 | **Kỹ sư Đồ thị tri thức (GraphRAG) & AI Agent:** *(Nhánh nghiên cứu song song)* Khảo sát tổng quan tài liệu, thiết kế Schema *Traffic Knowledge Graph* (Nút – Tuyến – Điểm ngập – Cảnh báo) và xây dựng demo Agent hỗ trợ tư vấn lộ trình. |

---

## I. NỘI DUNG ĐỀ TÀI

### 1. Tổng quan đề tài & Tính cấp thiết
Tại các đô thị loại đặc biệt như Thành phố Hồ Chí Minh, ùn tắc giao thông là một vấn nạn nhức nhối gây thiệt hại hàng ngàn tỷ đồng mỗi năm về kinh tế, nhiên liệu và ô nhiễm môi trường. Đặc biệt, giao thông TP.HCM mang hai nét đặc thù rõ nét:
1. **Mật độ xe máy hỗn hợp cực cao và cấu trúc nút giao đồng mức phức tạp:** Khi một nút giao thông trọng điểm bị quá tải (tiêu biểu như cụm Ngã tư Hàng Xanh – Đinh Bộ Lĩnh – Xô Viết Nghệ Tĩnh – Điện Biên Phủ), hiện tượng "dồn toa" xảy ra nhanh chóng, biến một điểm nghẽn cục bộ thành một **làn sóng ùn tắc (Congestion Wave)** lan truyền ngược dòng hoặc xuôi dòng sang các trục đường lân cận chỉ sau 15–30 phút.
2. **Tác động phi tuyến tính của thời tiết nhiệt đới (mưa to và triều cường):** Các cơn mưa lớn trên $30\text{ mm/h}$ kết hợp triều cường sông Sài Gòn làm tê liệt các đoạn trũng thấp (như đường Đinh Bộ Lĩnh, Xô Viết Nghệ Tĩnh đoạn gần cầu Bình Triệu). Vận tốc phương tiện sụt giảm đột ngột, làm tốc độ lan truyền của sóng ùn tắc tăng vọt so với ngày nắng ráo.

#### Khoảng trống nghiên cứu & thực tiễn (Market & Research Gap):
Các ứng dụng bản đồ phổ biến hiện nay (như Google Maps, Vietmap) chủ yếu cung cấp **thông tin giao thông tĩnh tức thời** (dựa trên GPS của điện thoại người dùng hiển thị vạch màu xanh/cam/đỏ tại thời điểm tra cứu). Khi người lái xe nhìn thấy một đoạn đường báo đỏ thì sóng ùn tắc thực tế đã lan rộng sang các tuyến kế cận. Các hệ thống này **chưa có khả năng mô hình hóa động học lan truyền sóng** dựa trên cấu trúc liên kết đồ thị đường bộ và **chưa dự báo trước được sau bao lâu sóng ùn tắc sẽ ập đến nút tiếp theo khi trời mưa**.

Hơn nữa, theo định hướng giảng dạy của **Thầy Đặng Việt Dũng** trong môn *Máy học nâng cao*, các mô hình học máy hiện đại không được dừng lại ở mức "hộp đen" chỉ đưa ra con số dự đoán mà bắt buộc phải có **khả năng giải thích được (Explainability - XAI)**: giải thích rõ tại sao mô hình dự báo nút tiếp theo sẽ kẹt, do lượng mưa hay do xung đột lưu lượng từ nhánh nào đổ về, đồng thời có thể kết nối với **Đồ thị tri thức (Knowledge Graph)** để suy luận và cảnh báo lộ trình.

#### Khảo sát các nghiên cứu liên quan:
* **2 Bài báo nghiên cứu quốc tế:**
  1. *IEEE Transactions on Intelligent Transportation Systems (2023) – "Spatial-Temporal Graph Convolutional Networks: A Deep Learning Framework for Traffic Forecasting" (STGCN):* Công trình chứng minh rằng mạng lưới đường bộ bản chất là một đồ thị phi Euclid ($G = (V, E)$). Việc kết hợp tích chập đồ thị trong không gian (Spatial Graph Convolution) với tích chập theo chuỗi thời gian (Temporal Gated Convolution) giúp nắm bắt chính xác quy luật lan truyền lưu lượng vượt trội hơn hẳn các mô hình chuỗi thời gian truyền thống (ARIMA, LSTM).
  2. *Information Fusion / Elsevier (2024) – "Multi-modal Traffic Congestion Propagation Modeling under Extreme Weather Conditions using Graph Attention Networks":* Nghiên cứu tập trung vào bài toán dung hợp đa phương thức: tích hợp các biến ngoại sinh thời tiết (cường độ mưa, tốc độ gió, độ ẩm) vào ma trận trọng số cạnh động của đồ thị giao thông, chứng minh rằng lượng mưa làm thay đổi căn bản ma trận lan truyền sóng ùn tắc giữa các nút giao kề cận.
* **2 Nghiên cứu và đồ án trong nước:**
  1. *Tạp chí Giao thông Vận tải Việt Nam (2023) – "Mô hình hóa và dự báo điểm nghẽn giao thông đô thị tại TP.HCM trong điều kiện ngập nước do triều cường và mưa lớn":* Nghiên cứu đã khảo sát thực địa các điểm nghẽn ngập nước tại khu vực Bình Thạnh, chỉ ra mối tương quan phi tuyến giữa vũ lượng mưa, đỉnh triều cường và sự suy giảm vận tốc lưu thông trung bình từ $35\text{ km/h}$ xuống dưới $8\text{ km/h}$.
  2. *Kỷ yếu Hội nghị Khoa học Công nghệ Trẻ (Trường ĐH Công nghệ Thông tin, ĐHQG-HCM, 2024) – "Ứng dụng học máy và đồ thị tri thức trong phân tích mạng lưới giao thông đô thị":* Đề tài đề xuất việc biểu diễn các mối quan hệ ngữ nghĩa giữa nút giao, tuyến đường và sự kiện giao thông dưới dạng Knowledge Graph để phục vụ việc truy vấn thông minh và giải thích nguyên nhân ùn tắc.

#### Xác định vấn đề cần giải quyết:
1. Xây dựng đồ thị mạng lưới đường giao thông chuẩn hóa ($G = (V, E)$) cho cụm nút giao thông trọng điểm Hàng Xanh (TP.HCM) từ dữ liệu OpenStreetMap (OSMnx).
2. Thiết lập quy trình chọn lọc đặc trưng đa phương thức thông minh (*Feature Selection* gồm Pearson $r$, Variance Threshold, One-Hot, $\chi^2$, PCA) để lọc ra các đặc trưng thời tiết và giao thông cốt lõi.
3. Huấn luyện và so sánh các mô hình học máy (Baseline ML: Random Forest, LightGBM/XGBoost; mô hình học sâu đồ thị) dự báo xác suất và thời gian lan truyền sóng ùn tắc sang các nút kề cận sau 15, 30, 45, 60 phút.
4. Áp dụng SHAP values và Feature Importance để minh bạch hóa mô hình (khắc phục tính hộp đen), chỉ rõ mức độ tác động của biến mưa/ngập tới việc kích hoạt sóng ùn tắc.
5. Tổ chức trạng thái nút giao thành Đồ thị tri thức (*Traffic Knowledge Graph*) và thử nghiệm Agent thông minh hỗ trợ truy vấn cảnh báo lộ trình thay thế (bám sát nội dung Chặng 3 của Thầy Dũng).

#### Sơ đồ tổng quan kiến trúc giải pháp (Tự chủ trong CS315):
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│           SƠ ĐỒ TỔNG QUAN HỆ THỐNG ĐỒ ÁN CS315 - MÁY HỌC NÂNG CAO (ĐỘC LẬP)            │
└────────────────────────────────────────────────────────────────────────────────────────┘

 [ TẦNG 1: THU THẬP & LÀM SẠCH DỮ LIỆU ]           [ TẦNG 2: CHỌN LỌC ĐẶC TRƯNG ]
 ┌──────────────────────────────────────┐          ┌──────────────────────────────────────┐
 │ 1. Đồ thị & Dữ liệu đầu vào (Python) │          │ 3. Chọn lọc đặc trưng thông minh     │
 │    - OSMnx: Cụm Hàng Xanh (15–25 nút)│          │    - Số: Variance Threshold, Pearson │
 │    - Thời tiết Open-Meteo & Triều PA │───────>  │    - Phân loại: One-Hot & Chi2 (5.99)│
 │    - Tập chuẩn METR-LA (đối chứng)   │          │    - Nhánh đối chứng giảm chiều PCA  │
 │    - Hàng Xanh (mô phỏng tăng cường) │          └──────────────────┬───────────────────┘
 └──────────────────────────────────────┘                             │
                                                                      ▼
 ┌──────────────────────────────────────┐          ┌──────────────────────────────────────┐
 │ 5. Giải thích mô hình (XAI) & KG    │          │ 4. Mô hình hóa Lan truyền sóng       │
 │    - SHAP values (chống Hộp đen)     │ <─────── │    - Baseline ML: RF / LightGBM      │
 │    - Traffic Knowledge Graph (KG)    │          │    - Spatial-Temporal Graph Model    │
 │    - AI Agent cảnh báo lộ trình      │          │    - TimeSeriesSplit + Recall / F1   │
 └──────────────────────────────────────┘          └──────────────────────────────────────┘
```

---

### 2. Mục tiêu của đề tài

#### Mục tiêu tổng quát:
Xây dựng thành công hệ thống học máy có khả năng mô hình hóa mạng lưới đường bộ đô thị TP.HCM thành cấu trúc đồ thị, kết hợp dữ liệu thời tiết đa phương thức để dự báo chính xác sự lan truyền của làn sóng ùn tắc qua các nút kề cận theo thời gian thực (15–60 phút), đồng thời giải thích được nguyên nhân gây tắc nghẽn và đưa ra cảnh báo ngữ nghĩa thông qua đồ thị tri thức.

#### 4 Mục tiêu kỹ thuật cụ thể:
1. **Lựa chọn đặc trưng đầu vào bài bản (Feature Selection):** Áp dụng chuẩn xác các kỹ thuật đã học ở Buổi 2 (*Filter*: Variance Threshold, Pearson $r$; *Categorical Encoding*: One-Hot; Giảm chiều: $\chi^2$ test, PCA) để rút gọn không gian đặc trưng từ hàng chục biến thô xuống tập đặc trưng tinh gọn, giúp giảm chi phí tính toán và chống quá khớp (*Overfitting*).
2. **Mô hình hóa dự báo lan truyền sóng chính xác & tối ưu độ nhạy:** Huấn luyện các mô hình học máy dự báo mức độ ùn tắc tại các nút lân cận sau các khoảng trễ $15', 30', 45', 60'$. Đạt độ nhạy `Recall` $\ge 85\%$ và `F1-Score` $\ge 80\%$ đối với các pha ùn tắc nghiêm trọng (không bỏ sót cảnh báo sớm).
3. **Minh bạch hóa mô hình (Explainability - XAI):** Triển khai SHAP values giải thích định lượng đóng góp của từng yếu tố (lượng mưa $mm/h$, khung giờ cao điểm, lưu lượng nút nguồn) đối với dự báo tại từng nút đích, giải quyết triệt để vấn đề "hộp đen" của AI.
4. **Khai thác Đồ thị tri thức & AI Agent (Bám sát Chặng 3):** Xây dựng cấu trúc *Traffic Knowledge Graph* mô tả quan hệ giữa Nút giao – Tuyến đường – Điểm ngập nước – Sự kiện ùn tắc; thử nghiệm Agent gọi công cụ (*Tool-calling*) tra cứu và đề xuất lộ trình thay thế né sóng kẹt xe.

---

### 3. Phương pháp thực hiện

* **Phương pháp nghiên cứu lý thuyết & tài liệu:**
  * Nghiên cứu cơ sở toán học của các thuật toán chọn đặc trưng: Hệ số tương quan Pearson, ngưỡng phương sai, kiểm định độc lập Chi-bình phương ($\chi^2$), phân tích thành phần chính (PCA).
  * Nghiên cứu lý thuyết biểu diễn đồ thị không gian - thời gian (Spatial-Temporal Graph), ma trận kề có hướng $A \in \mathbb{R}^{N \times N}$ và cơ chế lan truyền tín hiệu trên đồ thị.
  * Nghiên cứu phương pháp giải thích mô hình SHAP (Shapley Additive exPlanations) dựa trên lý thuyết trò chơi hợp tác.
* **Phương pháp thu thập và tiền xử lý dữ liệu (Tự chủ 2 nhánh dữ liệu trong CS315):**
  * **Nhánh 1 — Tập chuẩn công khai đối chứng (`METR-LA`):** Sử dụng tập dữ liệu cảm biến giao thông công khai `METR-LA` (kèm ma trận kề đồ thị và chuỗi vận tốc đo đạc thực tế) để kiểm chứng khách quan hiệu năng các mô hình Baseline ML và ST-GNN trước khi áp dụng cho kịch bản TP.HCM.
  * **Nhánh 2 — Kịch bản đặc thù TP.HCM (Cụm Hàng Xanh):** Sử dụng thư viện `OSMnx` trích xuất đồ thị mạng lưới đường thực tế tại khu vực Hàng Xanh – Bình Thạnh (tọa độ nút, chiều dài đoạn đường, số làn xe, tốc độ tối đa); thu thập thời tiết thật từ `Open-Meteo Historical Weather API` (lượng mưa theo giờ $mm/h$, độ ẩm, nhiệt độ) kết hợp bảng lịch mực nước triều cường trạm Phú An trùng mốc ngày; sau đó xây dựng chuỗi lưu lượng Hàng Xanh mô phỏng tăng cường theo phân phối thực tế (giờ cao điểm, mưa ngập).
  * **Tiền xử lý thống nhất bằng Python (`Pandas`, `Scikit-learn`):** Kiểm tra khuyết thiếu, lọc ngoại lai, quy đổi múi giờ `UTC+7`, đồng bộ bước thời gian 15 phút và chuẩn hóa thành dạng bảng sạch.
* **Phương pháp thực nghiệm mô hình hóa:**
  * Xây dựng kịch bản chia dữ liệu chống rò rỉ thông tin tương lai: Sử dụng `TimeSeriesSplit` (Walk-forward Validation) thay vì K-Fold ngẫu nhiên để tôn trọng tính tuần tự thời gian.
  * Huấn luyện mô hình cơ sở (Baseline ML): Random Forest, LightGBM, XGBoost trên tập đặc trưng đã chọn lọc.
  * Thử nghiệm mô hình học sâu trên đồ thị (ST-GNN nhẹ) kết hợp ma trận kề tĩnh và ma trận trọng số động theo thời tiết.
* **Phương pháp kiểm thử và QA:**
  * Kiểm soát tiến độ theo tiêu chuẩn Definition of Done (DoD).
  * Đánh giá hiệu năng bằng bộ chỉ số đa chiều: `Precision`, `Recall`, `F1-Score`, `Macro-F1`, Ma trận nhầm lẫn (`Confusion Matrix`), và đường cong `PR-AUC` trên tập dữ liệu mất cân bằng.
  * Đo đạc thời gian huấn luyện và độ trễ suy luận (`Inference Latency`) trên Google Colab T4 đảm bảo đáp ứng yêu cầu dự báo thời gian thực ($< 500\text{ms}$).

---

### 4. Các nội dung chính của đề tài

* **Nội dung 1: Khảo sát tổng quan, thu thập dữ liệu và trích xuất đồ thị mạng lưới đường HCMC**
  * *Thực hiện cái gì:* Trích xuất đồ thị mạng lưới đường khu vực cụm Hàng Xanh ($G = (V, E)$ gồm $\approx 15 - 25$ nút giao và các đoạn đường kết nối); thu thập chuỗi thời gian vận tốc lưu thông và dữ liệu thời tiết mưa ngập.
  * *Thực hiện như thế nào:* Dùng `OSMnx` và `NetworkX` trên Python để lấy tọa độ và ma trận khoảng cách cụm Hàng Xanh; kết nối API thời tiết `Open-Meteo` và số hóa bảng lịch triều cường trạm Phú An; xây dựng bộ dữ liệu giao thông Hàng Xanh mô phỏng tăng cường theo phân phối thực tế đồng thời chuẩn hóa tập cảm biến thật `METR-LA` bằng `Pandas`/`Scikit-learn` để đối chứng thực nghiệm.
  * *Dự kiến kết quả:* Ma trận kề đồ thị chuẩn hóa $A$, danh sách nút $V$, tập cạnh $E$ và bộ dữ liệu giao thông - thời tiết dạng bảng sạch sẵn sàng cho bước chọn đặc trưng.
* **Nội dung 2: Lựa chọn đặc trưng thông minh (Feature Selection) và mã hóa biến phân loại**
  * *Thực hiện cái gì:* Loại bỏ các đặc trưng dư thừa và tĩnh; đo lường tương quan tuyến tính giữa các biến thời tiết, vận tốc với mức độ ùn tắc; mã hóa các biến phân loại và giảm chiều dữ liệu.
  * *Thực hiện như thế nào:* Áp dụng `VarianceThreshold` loại bỏ các cột phương sai thấp; tính ma trận hệ số tương quan Pearson $r$ (lọc các biến $|r| \ge 0.5$); áp dụng `OneHotEncoder` cho biến loại đường/hướng tuyến; thực hiện kiểm định Chi-bình phương ($\chi^2$) giữ lại các đặc trưng phân loại có ý nghĩa thống kê ($p < 0.05$); áp dụng `PCA` nén không gian nếu cần.
  * *Dự kiến kết quả:* Notebook `01_Feature_Selection.ipynb` hoàn chỉnh; bảng đối chiếu số lượng chiều dữ liệu trước và sau lọc; bảng xếp hạng mức độ quan trọng thống kê của các đặc trưng.
* **Nội dung 3: Thiết kế, huấn luyện đa mô hình học máy dự báo lan truyền sóng ùn tắc**
  * *Thực hiện cái gì:* Xây dựng bài toán phân loại đa lớp/dự báo mức độ ùn tắc (Thông thoáng, Ùn ứ, Kẹt xe nghiêm trọng) tại nút $v$ ở các thời điểm $t + 15', t + 30', t + 60'$ khi nút nguồn $u$ bị nghẽn.
  * *Thực hiện như thế nào:* Huấn luyện các mô hình Baseline ML (Random Forest, LightGBM, XGBoost) và mô hình tích hợp đồ thị; sử dụng kỹ thuật xử lý mất cân bằng lớp (SMOTE / Class Weighting); tinh chỉnh siêu tham số bằng Random Search kết hợp `TimeSeriesSplit`.
  * *Dự kiến kết quả:* Notebook `02_Model_Training.ipynb`; các file trọng số mô hình đã huấn luyện; bảng so sánh chi tiết hiệu năng giữa các thuật toán.
* **Nội dung 4: Thẩm định mô hình và giải thích kết quả dự báo (Explainable AI - XAI)**
  * *Thực hiện cái gì:* Đánh giá độ tin cậy của mô hình trên các kịch bản thời tiết khắc nghiệt; bóc tách tính hộp đen bằng cách giải thích nguyên nhân dự báo cho từng trường hợp cụ thể.
  * *Thực hiện như thế nào:* Vẽ ma trận nhầm lẫn (`Confusion Matrix`), phân tích `Recall` và `F1-Score` của lớp kẹt xe nặng; sử dụng thư viện `SHAP` (TreeExplainer) để vẽ biểu đồ tổng hợp (*Summary Plot*) và biểu đồ đóng góp lực (*Force Plot*) cho từng nút giao.
  * *Dự kiến kết quả:* Bộ biểu đồ SHAP chứng minh định lượng vai trò của lượng mưa và triều cường tới việc đẩy nhanh sóng kẹt xe; khẳng định tính minh bạch của giải pháp.
* **Nội dung 5: Xây dựng Đồ thị tri thức (Traffic Knowledge Graph) & AI Agent cảnh báo (Chặng 3)**
  * *Thực hiện cái gì:* Xây dựng cơ sở tri thức đồ thị mô tả mối quan hệ ngữ nghĩa giữa Nút giao – Tuyến đường – Khu vực ngập nước – Lộ trình thay thế; tạo AI Agent tra cứu trạng thái và đề xuất đường đi né sóng ùn tắc.
  * *Thực hiện như thế nào:* Thiết kế Ontology/Schema đồ thị tri thức trên `NetworkX` / `Neo4j`; tích hợp mô hình ngôn ngữ kết hợp kỹ thuật gọi công cụ (*Tool-calling*) tra cứu kết quả dự báo từ mô hình ML ở Nội dung 3 để sinh câu trả lời cảnh báo tự nhiên.
  * *Dự kiến kết quả:* Notebook `03_Traffic_KG_Agent_Demo.ipynb` chạy demo thành công kịch bản: *"Ngã tư Hàng Xanh đang kẹt nặng kèm mưa to, Agent phân tích sóng lan truyền và khuyến nghị rẽ hướng đường D2 thay vì Đinh Bộ Lĩnh"*.
* **Nội dung 6: Trực quan hóa bản đồ nhiệt, viết báo cáo tổng kết và nghiệm thu đồ án**
  * *Thực hiện cái gì:* Xây dựng giao diện demo trực quan hóa sóng ùn tắc lan truyền trên bản đồ số; viết toàn văn Báo cáo đồ án môn học (Word/PDF 40–50 trang) và thiết kế Slide báo cáo.
  * *Thực hiện như thế nào:* Dùng `Folium` / `Streamlit` hiển thị bản đồ nhiệt (Heatmap) lan truyền theo mốc thời gian $15' - 30' - 60'$; tổng hợp toàn bộ kết quả thực nghiệm, cấu trúc hóa báo cáo đúng chuẩn khoa học UIT; diễn tập thuyết trình nhóm.
  * *Dự kiến kết quả:* Quyển Báo cáo đồ án hoàn chỉnh; bộ Slide thuyết trình chuyên nghiệp; kho mã nguồn GitHub sạch sẽ kèm hướng dẫn tái lập kết quả; video clip demo sản phẩm.

---

### 5. Giới hạn của đề tài

* **Giới hạn không gian địa lý:** Nghiên cứu tập trung thử nghiệm trên mạng lưới đường đô thị thuộc **Cụm giao thông Ngã tư Hàng Xanh và các trục xuyên tâm lân cận** (thuộc Quận Bình Thạnh, TP.HCM), bao gồm các tuyến: Xô Viết Nghệ Tĩnh, Đinh Bộ Lĩnh, Bạch Đằng, Điện Biên Phủ, Nguyễn Gia Trí (D2), Ung Văn Khiêm. Không mở rộng toàn bộ 24 quận huyện để đảm bảo chất lượng đo kiểm sâu.
* **Giới hạn về dữ liệu:** Do TP.HCM chưa có bộ cảm biến giao thông công khai liên tục theo từng nút giao, đồ án triển khai song song 2 nhánh nguồn: (1) Tập cảm biến giao thông công khai **`METR-LA`** để kiểm chứng khách quan hiệu năng thuật toán trên chuỗi đo đạc thực tế; và (2) Bộ dữ liệu kịch bản **Cụm Hàng Xanh** kết hợp khung hình học thật (`OSMnx`), khí tượng vệ tinh thật (`Open-Meteo`), bảng lịch triều cường trạm Phú An và chuỗi lưu lượng mô phỏng tăng cường theo phân phối giờ cao điểm – mưa ngập TP.HCM.
* **Giới hạn phần cứng & môi trường thực thi:** Toàn bộ pipeline huấn luyện mô hình, trích xuất đặc trưng và đồ thị tri thức được thiết kế để chạy mượt mà trên môi trường máy trạm cá nhân hoặc **Google Colab miễn phí (GPU T4 / CPU)**, không đòi hỏi cụm máy chủ chuyên dụng đắt tiền.
* **Giới hạn chức năng:** Hệ thống tập trung vào bài toán **Dự báo lan truyền sóng ùn tắc & Giải thích nguyên nhân & Cảnh báo lộ trình tĩnh/động**; không can thiệp trực tiếp vào việc điều khiển chu kỳ đèn tín hiệu giao thông thực địa.

---

### 6. Đối tượng và phạm vi nghiên cứu

* **Đối tượng nghiên cứu:**
  * Đồ thị mạng lưới đường bộ đô thị $G = (V, E)$, ma trận kề $A$ và vector thuộc tính nút/cạnh theo thời gian.
  * Các thuật toán lựa chọn đặc trưng: Pearson Correlation, Variance Threshold, One-Hot Encoding, Chi-Square Test, PCA.
  * Các kiến trúc mô hình học máy: Random Forest, Gradient Boosting (LightGBM/XGBoost), Spatial-Temporal Graph Neural Networks.
  * Phương pháp giải thích mô hình: SHAP (Shapley Additive exPlanations).
  * Mô hình Đồ thị tri thức (*Knowledge Graph*) và Hệ thống tác tử (*Agentic AI*).
* **Phạm vi nghiên cứu:** Ứng dụng Trí tuệ nhân tạo và Học máy nâng cao trong lĩnh vực Giao thông thông minh (Intelligent Transportation Systems - ITS) tại đô thị TP.HCM.

---

### 7. Kết quả mong đợi

* **Về sản phẩm mô hình & thuật toán:**
  * Pipeline chọn lọc đặc trưng đa phương thức hoàn chỉnh, giảm thiểu tối thiểu $40\%$ số chiều dư thừa mà không làm suy giảm hiệu năng mô hình.
  * Mô hình học máy dự báo lan truyền sóng ùn tắc đạt độ nhạy `Recall` $\ge 85\%$ và `F1-Score` $\ge 80\%$ đối với các pha ùn tắc nghiêm trọng.
  * Báo cáo giải thích mô hình định lượng bằng SHAP, chỉ ra được ngưỡng mưa $mm/h$ bắt đầu kích hoạt sóng ùn tắc diện rộng.
* **Về sản phẩm phần mềm & demo:**
  * Bản đồ nhiệt trực quan hóa động thái lan truyền sóng ùn tắc theo thời gian ($15' - 30' - 60'$) trên nền tảng Folium / Web App trực quan.
  * Bản demo tương tác hỏi đáp với Traffic Knowledge Graph & Agent cảnh báo lộ trình thay thế.
* **Về tài liệu báo cáo:**
  * Một cuốn Báo cáo đồ án môn học đúng chuẩn quy định của Trường ĐH Công nghệ Thông tin (khoảng 40–50 trang), trình bày mạch lạc từ cơ sở lý thuyết, phương pháp, kết quả thực nghiệm đến kết luận.
  * Slide báo cáo thuyết trình chỉn chu (25–30 slide) kèm trọn bộ mã nguồn mở trên GitHub có file `README.md` hướng dẫn chạy lại kết quả.

---

## II. KẾ HOẠCH THỰC HIỆN CHI TIẾT (BẢNG TIẾN ĐỘ RÚT GỌN TỐI ĐA ĐẾN HẾT TUẦN 8)

Nhóm áp dụng mô hình phân công song song tăng tốc (*Fast-track Sprint*), nén toàn bộ quy trình nghiên cứu, thực nghiệm và hoàn thiện sản phẩm **về đích trọn vẹn vào cuối Tuần 8 (15/12/2026)**, giải phóng 100% áp lực trước các tuần thi cuối kỳ:

| Tuần | Thời Gian | Nội Dung Công Việc Cụ Thể (Fast-track) | Thành Viên Phụ Trách | Sản Phẩm Bàn Giao | Mức Độ |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **Tuần 3** | 04/11 – 10/11/2026 | Khởi tạo đề tài, viết Thuyết minh Đề cương chi tiết (MD) & Lập kế hoạch thực hiện đồ án (XLSX); chuẩn hóa đề tài lên file lớp `DS_Nhom_CS315.G12.LT.TTNT.xlsx`. | **Trần Hoàng Hôn** (Lead) & Cả nhóm | • File Đề cương chi tiết (MD)<br>• File Kế hoạch thực hiện (XLSX)<br>• Dòng đăng ký chuẩn trên sheet lớp | **0%** |
| **Tuần 4** | 11/11 – 17/11/2026 | • Trích xuất đồ thị OSMnx cụm Hàng Xanh (Nodes, Edges, Ma trận kề).<br>• Dựng khung trực quan hóa bản đồ GIS (Folium) kiểm tra tọa độ nút thực địa.<br>• Thiết lập pipeline thử nghiệm Baseline ML & hàm đo kiểm Recall/F1.<br>• Khảo sát tài liệu nghiên cứu quốc tế & thiết kế Schema Đồ thị tri thức.<br>• Tham vấn Thầy Dũng trực tiếp cuối buổi học 13/11. | • **Trần Hoàng Hôn**<br>• **Nguyễn Duy Khang**<br>• **Phạm Thành Trung**<br>• **Vũ Văn Duy**<br>• **Hoàng Cao Sơn** | • File ma trận đồ thị Hàng Xanh<br>• Bản đồ GIS trực quan tọa độ nút<br>• Mock pipeline huấn luyện & hàm Recall<br>• Bản thảo Schema Traffic KG<br>• Biên bản góp ý của Thầy | **0%** |
| **Tuần 5** | 18/11 – 24/11/2026 | • Chuẩn hóa 2 nhánh dữ liệu sạch bằng Python (tập cảm biến thật `METR-LA` đối chứng & kịch bản Hàng Xanh: `OSMnx` + `Open-Meteo` + lịch triều cường Phú An + giao thông mô phỏng tăng cường) & hoàn thành dứt điểm Feature Selection (Variance Threshold, Pearson $r$, One-Hot, $\chi^2$, nhánh đối chứng PCA).<br>• Huấn luyện và đánh giá các mô hình Baseline ML (Random Forest, LightGBM, XGBoost) dự báo lan truyền sau $15' - 30' - 60'$.<br>• Dựng cơ sở dữ liệu Đồ thị tri thức mẫu trên NetworkX. | • **Nguyễn Duy Khang**<br>• **Phạm Thành Trung**<br>• **Hoàng Cao Sơn**<br>• **Vũ Văn Duy** | • Notebook `01_Feature_Selection.ipynb`<br>• Dataset đã chọn lọc đặc trưng<br>• Trọng số mô hình Baseline (.pkl/.json)<br>• Bảng tương quan thống kê & Recall ban đầu | **0%** |
| **Tuần 6** | 25/11 – 01/12/2026 | • Nâng cấp mô hình đồ thị / Ensemble học máy, tối ưu độ nhạy Recall $\ge 85\%$ & F1-Score cho các pha kẹt xe nghiêm trọng.<br>• Áp dụng SHAP values (TreeExplainer) bóc tách định lượng tác động của lượng mưa & triều cường (khắc phục tính hộp đen).<br>• Thử nghiệm AI Agent gọi công cụ (*Tool-calling*) tra cứu lộ trình thay thế né kẹt. | • **Phạm Thành Trung**<br>• **Vũ Văn Duy**<br>• **Hoàng Cao Sơn**<br>• **Trần Hoàng Hôn** | • Notebook `02_Model_Training.ipynb`<br>• Biểu đồ SHAP Summary & Force Plot<br>• Module AI Agent thử nghiệm<br>• Bản thảo Chương 2 & 3 Báo cáo | **0%** |
| **Tuần 7** | 02/12 – 08/12/2026 | • Xây dựng bản đồ nhiệt trực quan hóa động thái lan truyền sóng ùn tắc (Folium / Web App Streamlit).<br>• Hoàn thiện toàn diện module AI Agent tương tác tự nhiên hỏi - đáp lộ trình.<br>• Hoàn thành 100% nội dung quyển Báo cáo đồ án môn học (Word/PDF 40–50 trang).<br>• Đóng gói mã nguồn sạch sẽ lên GitHub nhóm có file `README.md`. | • **Vũ Văn Duy**<br>• **Hoàng Cao Sơn**<br>• **Trần Hoàng Hôn**<br>• **Phạm Thành Trung**<br>• **Nguyễn Duy Khang** | • Bản đồ nhiệt trực quan chạy mượt<br>• Notebook `03_Traffic_KG_Agent_Demo.ipynb`<br>• Toàn văn Báo cáo đồ án hoàn chỉnh<br>• Kho GitHub chuẩn hóa kèm dữ liệu mẫu | **0%** |
| **Tuần 8** | 09/12 – 15/12/2026 | • Thiết kế Slide thuyết trình chỉn chu (25–30 slide).<br>• Quay video clip demo kịch bản sóng ùn tắc Hàng Xanh khi trời mưa lớn.<br>• **BÁO CÁO VÀ NGHIỆM THU ĐỒ ÁN HOÀN TẤT VỚI GIẢNG VIÊN (ThS. Đặng Việt Dũng).**<br>• Nộp trọn bộ hồ sơ (Báo cáo Word/PDF + Slide + Source Code + Video Demo). | **Cả nhóm 5 thành viên** *(Trần Hoàng Hôn điều phối)* | • File Slide báo cáo (.pptx / .pdf)<br>• Video demo hoàn chỉnh<br>• Toàn bộ sản phẩm nộp trên Drive lớp<br>• **HOÀN THÀNH 100% ĐỒ ÁN MÔN HỌC** | **0%** |

*(Các tuần 9–11 còn lại dành trọn vẹn cho việc hiệu chỉnh nhỏ theo phản hồi của Thầy nếu có, ôn thi các học phần khác và không phát sinh thêm bất kỳ gánh nặng đồ án nào).*

---

### XÁC NHẬN CỦA CÁC BÊN

**CÁN BỘ HƯỚNG DẪN**  
*(Ký và ghi rõ họ tên)*  
<br><br><br><br>  
**ThS. Đặng Việt Dũng**

*TP. Hồ Chí Minh, ngày 11 tháng 11 năm 2026*  
**ĐẠI DIỆN NHÓM SINH VIÊN THỰC HIỆN**  
*(Ký và ghi rõ họ tên)*  
<br><br><br><br>  
**Trần Hoàng Hôn** *(Trưởng nhóm)*
