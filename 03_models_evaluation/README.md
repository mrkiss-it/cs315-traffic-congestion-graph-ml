# 03_models_evaluation — Huấn luyện mô hình ML/GNN & Giải thích XAI

* **Phụ trách chính:** Phạm Thành Trung (`[T3]`), Vũ Văn Duy (`[D2]`)
* **Sản phẩm dự kiến:**
  * `mock_ml_pipeline.py` (`[T3]`): chia `TimeSeriesSplit` theo `unique timestamp`, baseline `RandomForest`/`LightGBM` với `class_weight='balanced'`, đo `Recall` lớp `2`, `Macro-F1`, One-vs-Rest `PR-AUC` lớp `2` & `Confusion Matrix`
  * Smoke-test `shap.TreeExplainer` trên tên biến gốc (`[D2]`)
  * `02_Model_Training.ipynb` (Tuần 5–6): import module `.py` tại thư mục này để huấn luyện Baseline ML, ST-GNN và xuất biểu đồ SHAP

