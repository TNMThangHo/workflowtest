# 📘 TÀI LIỆU TEST CASE

---

**Thông tin chung:**

- **Feature:** {{ feature_name }}
- **Phiên bản PRD:** {{ prd_version }}
- **Ngày tạo:** {{ created_date }}
- **Người thực hiện:** {{ tester }}

---

## I. THỐNG KÊ TỔNG QUAN (DASHBOARD)

### 1. Tổng hợp số lượng

| Chỉ số                         | Giá trị                    |
| :----------------------------- | :------------------------- |
| **Tổng số Test Case**          | **{{ total_cases }}**      |
| Functional (Chức năng)         | {{ functional_count }}     |
| Non-Functional (Phi chức năng) | {{ non_functional_count }} |

### 2. Phân bố mức độ ưu tiên

| Mức độ                       | Số lượng       | Tỷ lệ (%)         |
| :--------------------------- | :------------- | :---------------- |
| **P0 (Critical - Blocker)**  | {{ p0_count }} | {{ p0_percent }}% |
| **P1 (Cao - High)**          | {{ p1_count }} | {{ p1_percent }}% |
| **P2 (Trung bình - Medium)** | {{ p2_count }} | {{ p2_percent }}% |
| **P3 (Thấp - Low)**          | {{ p3_count }} | {{ p3_percent }}% |

---

## II. KIỂM THỬ CHỨC NĂNG (FUNCTIONAL TESTING)

Dưới đây là danh sách chi tiết các kịch bản kiểm thử nghiệp vụ.

| ID  | Module | Title | Pre-condition | Step | Test Data | Expected Result | Status | Priority | Create Date | Execute Date |
| :-- | :----- | :---- | :------------ | :--- | :-------- | :-------------- | :----- | :------- | :---------- | :----------- |

{% for tc in functional_testcases -%}
| {{ tc.id }} | {{ tc.module }} | {{ tc.title }} | {{ tc.pre_condition }} | {{ tc.steps_short }} | {{ tc.test_data }} | {{ tc.expected_result }} | {{ '[ ] Pass <br> [ ] Fail' if tc.status in ['New', '[ ]', ''] else tc.status }} | {{ tc.priority }} | {{ tc.created_date }} | {{ tc.execute_date }} |
{% endfor -%}

---

## III. KIỂM THỬ PHI CHỨC NĂNG (NON-FUNCTIONAL TESTING)

### 1. Phạm vi kiểm thử

Các nhóm tiêu chí phi chức năng được bao phủ trong tài liệu này:
_(Được đánh dấu tự động dựa trên kết quả phân tích)_

- [{{ 'x' if 'Performance' in nft_categories else ' ' }}] **Performance** (Hiệu năng)
- [{{ 'x' if 'Security' in nft_categories else ' ' }}] **Security** (Bảo mật)
- [{{ 'x' if 'Availability' in nft_categories else ' ' }}] **Availability** (Tính sẵn sàng)
- [{{ 'x' if 'Reliability' in nft_categories else ' ' }}] **Reliability** (Độ tin cậy)
- [{{ 'x' if 'Usability' in nft_categories else ' ' }}] **Usability** (Khả năng sử dụng)
- [{{ 'x' if 'Accessibility' in nft_categories else ' ' }}] **Accessibility** (Khả năng truy cập)
- [{{ 'x' if 'Compatibility' in nft_categories else ' ' }}] **Compatibility** (Tương thích)
- [{{ 'x' if 'Analytics' in nft_categories else ' ' }}] **Analytics** (Phân tích dữ liệu)

### 2. Danh sách Test Case chi tiết

| ID  | Category | Title | Tools/Env | Step | Pass Criteria | Status | Priority | Create Date | Execute Date |
| :-- | :------- | :---- | :-------- | :--- | :------------ | :----- | :------- | :---------- | :----------- |

{% for tc in non_functional_testcases -%}
| {{ tc.id }} | {{ tc.category }} | {{ tc.title }} | {{ tc.tools if tc.tools else tc.pre_condition }} | {{ tc.steps_short }} | {{ tc.pass_criteria if tc.pass_criteria else tc.expected_result }} | {{ '[ ] Pass <br> [ ] Fail' if tc.status in ['New', '[ ]', ''] else tc.status }} | {{ tc.priority }} | {{ tc.created_date }} | {{ tc.execute_date }} |
{% endfor -%}

---

## IV. GHI CHÚ & THEO DÕI LỖI (BUG TRACKING)

_(Phần này dành cho Tester ghi chú thủ công khi chạy test)_

### Danh sách Bug phát hiện:

| Bug ID | Liên kết (Jira/Issue) | Mức độ nghiêm trọng | Trạng thái |
| :----- | :-------------------- | :------------------ | :--------- |
|        |                       |                     |            |
|        |                       |                     |            |
