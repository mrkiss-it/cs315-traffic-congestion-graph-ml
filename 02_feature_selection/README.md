# 02_feature_selection — Data Contract & Lựa chọn đặc trưng

* **Phụ trách chính:** Nguyễn Duy Khang (`[K1]`, `[K2]`)
* **Sản phẩm dự kiến:**
  * `feature_dictionary.md`: schema cột, đơn vị, quy tắc nội suy `1h -> 15'`, phân loại biến số / *Ordinal* / *Nominal* và 3 cột nhãn `y_t15`, `y_t30`, `y_t60`
  * `01_feature_selection_pipeline.py`: module Python (nhánh số `VarianceThreshold` + `Pearson r`, nhánh phân loại + $\chi^2 > 5.99$, hàm `fit` theo từng fold `train`, nhánh đối chứng `PCA` tách riêng)
  * `01_Feature_Selection.ipynb` (Tuần 5): import module `.py` tại thư mục này

