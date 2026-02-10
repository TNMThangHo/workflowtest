# 📋 BÁO CÁO REVIEW TEST CASE - QUẢN LÝ DANH MỤC DỰ ÁN

---

## 📌 THÔNG TIN CHUNG

| Thông tin | Chi tiết |
|-----------|----------|
| **Tên tính năng** | Quản lý Danh mục Dự án (Project Management) |
| **Phiên bản PRD** | 1.0 |
| **Ngày review** | 10/02/2026 |
| **Người review** | QA Lead |
| **File PRD** | projectPrd.md |
| **File Test Case** | tc4_e2e.md |

---

## 📊 TỔNG QUAN KẾT QUẢ

### Thống kê Coverage

| Chỉ số | Giá trị | Ghi chú |
|--------|---------|---------|
| **Tổng Test Case hiện tại** | 76 | |
| **Coverage ước tính** | ~35% | Dựa trên yêu cầu PRD |
| **Test Case cần bổ sung** | ~120-140 | Để đạt coverage đầy đủ |
| **Mức độ nghiêm trọng** | 🔴 HIGH | Thiếu các chức năng CORE |

### Đánh giá theo mức độ ưu tiên

| Mức độ | Test Case hiện có | Test Case cần thêm | Tổng dự kiến |
|--------|-------------------|-------------------|--------------|
| **P0 (Critical)** | 1 | 5-8 | 6-9 |
| **P1 (High)** | 12 | 30-35 | 42-47 |
| **P2 (Medium)** | 63 | 80-90 | 143-153 |
| **P3 (Low)** | 0 | 5-7 | 5-7 |

---

## ✅ CÁC PHẦN ĐÃ COVER TỐT

### 1. Danh sách dự án (Section 2 PRD) - Coverage: ~70%

#### ✅ Đã có:
- [x] Tìm kiếm theo Tên dự án, Mã dự án (TC-FUNC-001 → TC-FUNC-004)
- [x] Bộ lọc Vùng (TC-FUNC-010 → TC-FUNC-012)
- [x] Bộ lọc Khu vực (TC-FUNC-014 → TC-FUNC-016)
- [x] Bộ lọc Trạng thái (TC-FUNC-018 → TC-FUNC-022)
- [x] Bộ lọc Người quản lý (TC-FUNC-024 → TC-VALI-025)
- [x] Validation input (Max length, Trim, Unicode, XSS, SQL injection)
- [x] Security testing đầy đủ (TC-SECU-005 → TC-SECU-058)
- [x] Business logic: Filter dependency Region → Area (TC-BUSI-060)
- [x] Business logic: Project list visibility (TC-BUSI-059)

#### ❌ Còn thiếu:
- [ ] Chức năng Sắp xếp (Mặc định: Ngày tạo Mới→Cũ, Tùy chỉnh: Tên A-Z)
- [ ] Hiển thị tiến trình pháp lý (%) - Progress bar
- [ ] Import danh sách dự án từ file
- [ ] Menu thao tác (Mở chi tiết từng dự án)
- [ ] Tạo dự án mới từ list view
- [ ] Pagination/Load more

---

### 2. Tạo dự án mới (Section 4 PRD) - Coverage: ~60%

#### ✅ Đã có:
- [x] Validation Vùng (Required) (TC-VALI-031)
- [x] Validation Khu vực (Required) (TC-VALI-036)
- [x] Select Vùng options (TC-FUNC-032 → TC-FUNC-034)
- [x] Select Khu vực options (TC-FUNC-038 → TC-FUNC-040)
- [x] Validation Tên dự án (TC-FUNC-041 → TC-VALI-044)
- [x] Validation Mã dự án (TC-FUNC-050 → TC-FUNC-051)
- [x] Select Người quản lý (TC-FUNC-057)
- [x] Business logic: Manager selection theo Vùng/Khu vực (TC-BUSI-061)
- [x] Business logic: Auto permission assignment (TC-BUSI-062)
- [x] E2E Happy path (TC-E2E-069)
- [x] Security testing (XSS, SQL injection cho các trường input)

#### ❌ Còn thiếu:
- [ ] Validation Chủ đầu tư (Required)
- [ ] Validation Loại dự án (Required)
- [ ] Validation Ngày bắt đầu/Kết thúc
- [ ] Validation Ngày kết thúc > Ngày bắt đầu
- [ ] Trường Tags (Multi-select, validation)
- [ ] Mô tả tổng quan (Rich text editor?)
- [ ] Nội dung phục vụ thanh tra
- [ ] **Custom Fields (Trường tùy chọn):**
  - [ ] Hiển thị dynamic fields theo Vùng/Khu vực
  - [ ] Validation custom fields
  - [ ] Logic Soft Delete khi field bị ẩn/xóa
- [ ] **Biểu mẫu nội bộ:**
  - [ ] Chọn template theo Vùng/Khu vực
  - [ ] Preview cấu trúc template
  - [ ] Apply template vào dự án
- [ ] **Phân quyền ban đầu:**
  - [ ] Thêm User/Phòng ban
  - [ ] Chỉ hiển thị cùng Vùng/Khu vực
  - [ ] Gán quyền (Manage/View/Input/Download)
- [ ] Auto-generate Mã dự án
- [ ] Form validation tổng thể (Submit với các trường thiếu)

---

### 3. Non-functional Testing - Coverage: ~80%

#### ✅ Đã có:
- [x] Browser compatibility (Chrome, Firefox, Safari, Edge) (TC-COMP-070 → TC-COMP-073)
- [x] Responsive design (Mobile, Tablet, Desktop) (TC-COMP-074 → TC-COMP-076)
- [x] Security testing đầy đủ (XSS, SQL injection, Command injection, etc.)
- [x] Visual testing cơ bản (Progress bar, Status chips, Form layout)

#### ❌ Còn thiếu:
- [ ] Performance testing (Load time, API response time)
- [ ] Stress testing (1000+ projects in list)
- [ ] Concurrent user testing
- [ ] File upload performance (Large files)
- [ ] OCR processing time
- [ ] Accessibility testing (WCAG 2.1)

---

## 🔴 CÁC PHẦN THIẾU NGHIÊM TRỌNG

### 1. Tab "Thông tin & Tiến trình" (Section 3.1 PRD) - Coverage: ~5% ⚠️

**Mức độ nghiêm trọng:** 🔴 CRITICAL

#### ❌ Thiếu hoàn toàn:

##### A. Thông tin chung (Read-only mode)
- [ ] Hiển thị đầy đủ thông tin dự án
- [ ] Toggle chế độ View/Edit
- [ ] QR Code generation và functionality
  - [ ] Quét QR redirect đến dự án
  - [ ] Yêu cầu quyền truy cập
  - [ ] QR code download/print
- [ ] Hiển thị Loại dự án
- [ ] Hiển thị Đơn vị đầu tư
- [ ] Hiển thị Người quản lý
- [ ] Hiển thị Vùng – Khu vực
- [ ] Hiển thị Tags (clickable?)
- [ ] Hiển thị Ngày bắt đầu - Kết thúc dự kiến
- [ ] Hiển thị Mô tả tổng quan
- [ ] Hiển thị Nội dung phục vụ thanh tra
- [ ] Metadata: Ngày cập nhật gần nhất, Người cập nhật

##### B. Tiến trình dự án (Giai đoạn)
- [ ] Hiển thị danh sách Đợt/Giai đoạn
- [ ] Thông tin giai đoạn:
  - [ ] Thời gian thực hiện
  - [ ] Tên giai đoạn
  - [ ] Trạng thái (Hoàn thành/Đang thực hiện/Chưa bắt đầu)
- [ ] **Thanh tiến độ % (AUTO-CALCULATE):**
  - [ ] Công thức: (Công việc hoàn thành / Tổng công việc liên quan tài liệu trong Đợt) * 100%
  - [ ] Visual progress bar
  - [ ] Real-time update khi task hoàn thành
- [ ] Mapping Đợt với Hồ sơ (A, B, C)

**Số test case cần bổ sung:** ~15-20 (P1)

---

### 2. Tab "Quản lý Hồ sơ Dự án" (Section 3.2 PRD) - Coverage: ~2% ⚠️⚠️⚠️

**Mức độ nghiêm trọng:** 🔴🔴🔴 BLOCKER - Đây là chức năng CORE nhất!

#### ❌ Thiếu gần như toàn bộ:

##### A. Danh sách hồ sơ (Tree View)
- [ ] **Cấu trúc cây phân cấp:**
  - [ ] Nhóm hồ sơ (Level 0: A, B, C...)
  - [ ] Hồ sơ cấp 1 (Level 1: A.1, A.2...)
  - [ ] Hồ sơ cấp 2 (Level 2: A.1.1, A.1.2...)
  - [ ] Tài liệu (Leaf nodes)
- [ ] Expand/Collapse nodes
- [ ] Lazy loading cho large trees
- [ ] **Hiển thị thông tin cột:**
  - [ ] Tên
  - [ ] Mã hồ sơ
  - [ ] Độ mật (Công khai/Mật/Tối mật/Tuyệt mật)
  - [ ] Người phụ trách
  - [ ] Trạng thái
  - [ ] Ngày cập nhật cuối
- [ ] **Tìm kiếm trong tree:**
  - [ ] Search theo Tên
  - [ ] Search theo Mã
  - [ ] Search theo Người phụ trách
  - [ ] Highlight kết quả trong cây
  - [ ] Auto-expand đến node được tìm thấy
- [ ] **Bộ lọc:**
  - [ ] Filter theo Độ mật
  - [ ] Filter theo Trạng thái
  - [ ] Kết hợp nhiều filter

##### B. CRUD Thư mục
- [ ] **Thêm mới thư mục:**
  - [ ] Validation Tên thư mục (Required, Max length, Special chars)
  - [ ] Chọn Thư mục cha (Tree selector)
  - [ ] Chọn Độ mật (Dropdown)
  - [ ] Chọn Người phụ trách (Autocomplete)
  - [ ] Inherit độ mật từ thư mục cha?
- [ ] **Sửa thư mục:**
  - [ ] Cập nhật tên
  - [ ] Di chuyển vị trí (Change parent)
  - [ ] Thay đổi độ mật (Impact check cho children)
  - [ ] Thay đổi người phụ trách
- [ ] **Xóa thư mục:**
  - [ ] Cảnh báo nếu có thư mục con
  - [ ] Cảnh báo nếu có tài liệu
  - [ ] Cascade delete hoặc Move to parent
  - [ ] Permission check

##### C. CRUD Tài liệu
- [ ] **Tạo tài liệu:**
  - [ ] Validation Mã tài liệu (Required, Unique, Format)
  - [ ] Validation Tên tài liệu (Required, Max length)
  - [ ] Chọn Thư mục cha (Required)
  - [ ] Chọn Độ mật (Required)
  - [ ] Nhập Ghi chú (Optional, Rich text?)
- [ ] **Upload file:**
  - [ ] Hỗ trợ multiple file types (PDF, DOC, XLS, IMG...)
  - [ ] File size limit validation
  - [ ] Progress bar khi upload
  - [ ] **OCR Processing:**
    - [ ] Đổi nền màu vàng khi đang xử lý
    - [ ] Về màu mặc định khi hoàn thành
    - [ ] Error handling khi OCR fail
    - [ ] Extract text từ image/PDF
  - [ ] Virus scan
  - [ ] Auto-generate thumbnail
- [ ] **Sửa tài liệu:**
  - [ ] Cập nhật metadata
  - [ ] Di chuyển vị trí
  - [ ] Thay đổi độ mật
- [ ] **Xóa tài liệu:**
  - [ ] Soft delete hoặc Hard delete
  - [ ] Permission check
  - [ ] Impact check (Có task đang liên kết?)

##### D. Chi tiết tài liệu (Popup)
- [ ] **Hiển thị Siêu dữ liệu (Metadata):**
  - [ ] Tên file
  - [ ] Dung lượng (KB/MB/GB)
  - [ ] Loại file (Extension, MIME type)
  - [ ] Độ mật
  - [ ] Vị trí lưu trữ vật lý:
    - [ ] Tầng
    - [ ] Phòng
    - [ ] Tủ
    - [ ] Ngăn
  - [ ] Phiên bản hiện tại
  - [ ] Ngày tạo, Người tạo
  - [ ] Ngày cập nhật, Người cập nhật
- [ ] **Liên kết công việc:**
  - [ ] Danh sách công việc liên quan
  - [ ] Thông tin: Tên việc, Deadline, PIC, Tiến độ
  - [ ] Navigate to task detail
  - [ ] Filter/Sort tasks
- [ ] **Lịch sử phiên bản:**
  - [ ] Log thay đổi (Version 1, 2, 3... tự tăng)
  - [ ] Chi tiết thêm/xóa/sửa (+/- indicator)
  - [ ] Download phiên bản cũ
  - [ ] Compare versions (Diff view)
  - [ ] Restore phiên bản cũ
  - [ ] Timestamp và User cho mỗi version
- [ ] **Xem trước (Preview):**
  - [ ] PDF preview
  - [ ] Image preview
  - [ ] Office docs preview (Word, Excel, PPT)
  - [ ] Text file preview
  - [ ] Zoom in/out
  - [ ] Page navigation (cho multi-page docs)
- [ ] **Tải xuống:**
  - [ ] Permission check: Chỉ kích hoạt nếu user có quyền "Download" hoặc "Input"
  - [ ] Original filename preserved
  - [ ] Download log/audit trail

##### E. Tổ chức hồ sơ (Re-organize)
- [ ] **Giao diện kéo thả:**
  - [ ] Drag & drop trong cùng level
  - [ ] Drag & drop giữa các level
  - [ ] Visual feedback khi drag
  - [ ] Drop zone highlighting
  - [ ] Validation: Không cho drop vào child của chính nó
- [ ] **Sắp xếp lại thứ tự:**
  - [ ] Manual ordering
  - [ ] Save order preferences
- [ ] **Đánh dấu quan trọng:**
  - [ ] Icon "!" indicator
  - [ ] Filter by importance
  - [ ] Sort by importance
- [ ] **Context menu:**
  - [ ] Right-click menu
  - [ ] Rename
  - [ ] Delete
  - [ ] Move
  - [ ] Properties

##### F. Chia sẻ tài liệu (Sharing)
- [ ] **Scope:** Chỉ áp dụng cho Mật/Tối mật/Tuyệt mật
- [ ] **Thêm user vào danh sách chia sẻ:**
  - [ ] Search user (Autocomplete)
  - [ ] Search đơn vị
  - [ ] Multi-select
- [ ] **Gán quyền:**
  - [ ] Xem (View only)
  - [ ] Tải xuống (Download)
- [ ] **Quản lý danh sách chia sẻ:**
  - [ ] Xem danh sách đã chia sẻ
  - [ ] Revoke access
  - [ ] Update permissions
  - [ ] Expiry date cho share link?
- [ ] **Audit trail:**
  - [ ] Log ai đã xem
  - [ ] Log ai đã download
  - [ ] Timestamp

##### G. Xuất Excel
- [ ] Export cấu trúc cây ra file Excel
- [ ] Preserve hierarchy trong Excel
- [ ] Include metadata
- [ ] Column formatting
- [ ] Filter/export selected nodes only

**Số test case cần bổ sung:** ~50-60 (P0/P1) - URGENT!

---

### 3. Tab "Quản lý Công việc" (Section 3.3 PRD) - Coverage: 0% ⚠️⚠️

**Mức độ nghiêm trọng:** 🔴🔴 CRITICAL

#### ❌ Thiếu hoàn toàn:

##### A. Danh sách công việc
- [ ] **Hiển thị thông tin:**
  - [ ] Tên việc
  - [ ] Mã công việc
  - [ ] Giai đoạn (Đợt 1, 2, 3...)
  - [ ] Mức độ ưu tiên (Cao/Trung bình/Thấp)
  - [ ] Phân công (Assignee)
  - [ ] Trạng thái (Chưa bắt đầu/Đang làm/Hoàn thành...)
  - [ ] Tiến độ (%) với progress bar
  - [ ] Hạn cuối (Deadline)
  - [ ] **Highlight đỏ nếu quá hạn** ⚠️
- [ ] Pagination/Infinite scroll
- [ ] Sorting (By deadline, priority, status...)

##### B. Bộ lọc
- [ ] Filter theo Hình thức (Giao việc/Đặt hàng)
- [ ] Filter theo Mức độ ưu tiên (Multi-select)
- [ ] Filter theo Phân công (Assignee)
- [ ] Filter theo Trạng thái (Multi-select)
- [ ] Combine multiple filters
- [ ] Save filter preferences

##### C. Tạo việc mới
- [ ] **Loại: Giao việc**
  - [ ] Form fields validation
  - [ ] Chọn Giai đoạn
  - [ ] Chọn Mức độ ưu tiên
  - [ ] Phân công (Single/Multiple assignees)
  - [ ] Set deadline
  - [ ] Mô tả công việc
  - [ ] Attach tài liệu từ Hồ sơ
- [ ] **Loại: Đặt hàng**
  - [ ] Additional fields cho procurement
  - [ ] Budget/Cost fields
  - [ ] Vendor selection
- [ ] Auto-link task với tài liệu liên quan
- [ ] Notification to assignee

##### D. Sửa công việc
- [ ] Update task details
- [ ] Reassign task
- [ ] Change deadline
- [ ] Update progress %
- [ ] Change status
- [ ] Permission check (Only assignee or Manager)

##### E. Xóa công việc
- [ ] **Xóa đơn (Single delete):**
  - [ ] Confirmation popup
  - [ ] Permission check
  - [ ] Impact check (Có ảnh hưởng tiến độ dự án?)
- [ ] **Xóa nhiều (Bulk delete):**
  - [ ] Multi-select checkboxes
  - [ ] Batch delete confirmation
  - [ ] Progress indicator
  - [ ] Error handling (Một số task không thể xóa)

##### F. Tích hợp với Tiến độ dự án
- [ ] Khi task hoàn thành → Cập nhật % tiến trình Giai đoạn
- [ ] Real-time update progress bar
- [ ] Trigger notification
- [ ] Auto-update project status (Hoàn thành khi 100%)

**Số test case cần bổ sung:** ~25-30 (P1)

---

### 4. Tab "Phân quyền Dự án" (Section 3.4 PRD) - Coverage: ~10% ⚠️

**Mức độ nghiêm trọng:** 🔴 CRITICAL

#### ❌ Thiếu hầu hết:

##### A. Hiển thị danh sách quyền
- [ ] **Table view:**
  - [ ] Cột: Tên/Đơn vị
  - [ ] Cột: Loại (User/Unit) với icon phân biệt
  - [ ] Cột: Quyền hạn (Manage/View/Input/Download)
  - [ ] Avatar cho cá nhân
  - [ ] Số lượng nhân sự cho đơn vị
- [ ] **Logic hiển thị:**
  - [ ] Nếu User → Hiển thị Avatar + Tên
  - [ ] Nếu Đơn vị → Hiển thị Icon + Tên đơn vị + Số lượng thành viên
- [ ] **Cờ bảo hộ (ManageBy flag):**
  - [ ] Người tạo dự án có cờ "Owner"
  - [ ] Người quản lý có cờ "Manager"
  - [ ] Không hiển thị nút Xóa cho Owner/Manager
  - [ ] Tooltip giải thích tại sao không thể xóa

##### B. 4 loại quyền (Role Mapping)
- [ ] **1. Quản lý (Manage):**
  - [ ] Sửa thông tin dự án
  - [ ] Phân quyền cho người khác
  - [ ] Toàn quyền trên Hồ sơ/Công việc
  - [ ] Xóa dự án (Nếu là Admin)
- [ ] **2. Xem (View):**
  - [ ] Chỉ xem, không sửa
  - [ ] Không tải file (Chỉ Preview)
  - [ ] Không tạo/sửa task
  - [ ] Read-only mode trên tất cả tabs
- [ ] **3. Nhập liệu (Input):**
  - [ ] Sửa hồ sơ
  - [ ] Upload file
  - [ ] Download file
  - [ ] Tạo/sửa task (Nếu được assign)
- [ ] **4. Tải xuống (Download):**
  - [ ] Xem tất cả
  - [ ] Tải file
  - [ ] Không được sửa/upload

##### C. Thêm người/đơn vị
- [ ] **Thêm Cá nhân:**
  - [ ] Search user (Autocomplete)
  - [ ] **Điều kiện:** Chỉ hiển thị user thuộc Vùng/Khu vực của dự án
  - [ ] Chọn quyền (Radio buttons: Manage/View/Input/Download)
  - [ ] Validation: Không thêm trùng
  - [ ] Add button disabled khi chưa chọn quyền
- [ ] **Thêm Đơn vị:**
  - [ ] Search đơn vị (Dropdown)
  - [ ] **Điều kiện:** Chỉ hiển thị đơn vị thuộc Vùng/Khu vực của dự án
  - [ ] Chọn quyền
  - [ ] Auto-apply quyền cho tất cả thành viên đơn vị
  - [ ] Hiển thị số lượng thành viên sẽ được thêm
- [ ] Batch add (Multi-select users/units)

##### D. Sửa quyền
- [ ] Edit inline trong table
- [ ] Dropdown chọn quyền mới
- [ ] Confirmation khi thay đổi quyền từ Cao → Thấp
- [ ] Update permissions log

##### E. Xóa quyền
- [ ] **Xóa đơn:**
  - [ ] Confirmation popup
  - [ ] Check ManageBy flag (Không cho xóa Owner/Manager)
  - [ ] Remove permission
- [ ] **Xóa nhiều:**
  - [ ] Multi-select
  - [ ] Batch remove
  - [ ] Skip Owner/Manager (Show warning)

##### F. Permission Inheritance & Conflict
- [ ] Nếu user thuộc nhiều đơn vị → Lấy quyền cao nhất
- [ ] Nếu có quyền cá nhân + quyền đơn vị → Merge
- [ ] Show inherited permissions với indicator
- [ ] Tooltip giải thích nguồn gốc permission

**Số test case cần bổ sung:** ~20-25 (P1)

---

### 5. Chỉnh sửa & Xóa dự án (Section 5 PRD) - Coverage: ~20%

#### ✅ Đã có:
- [x] Delete confirmation (TC-BUSI-063)

#### ❌ Còn thiếu:

##### A. Chỉnh sửa dự án
- [ ] **Edit mode toggle:**
  - [ ] Nút Edit/Cancel/Save
  - [ ] Lock/Unlock fields
  - [ ] Dirty check (Cảnh báo nếu rời trang khi chưa save)
- [ ] **Cho phép sửa:**
  - [ ] Tên dự án
  - [ ] Loại dự án
  - [ ] Chủ đầu tư
  - [ ] Người quản lý (Impact: Auto-update Phân quyền)
  - [ ] Vùng/Khu vực (Impact check: Staff/Template)
  - [ ] Tags
  - [ ] Ngày bắt đầu/Kết thúc
  - [ ] Mô tả
  - [ ] Nội dung thanh tra
- [ ] **Custom Fields:**
  - [ ] Logic hiển thị field bị ẩn/xóa
  - [ ] Soft delete handling
  - [ ] Popup xác nhận khi field không còn valid
- [ ] **Validation khi save:**
  - [ ] Check required fields
  - [ ] Check data format
  - [ ] Check business rules
- [ ] **Trạng thái dự án:**
  - [ ] Cho phép chuyển trạng thái thủ công
  - [ ] Auto-update: Chuẩn bị (0%) → Đang thực hiện → Hoàn thành (100%)
  - [ ] Validation: Không cho chuyển Hoàn thành nếu chưa 100%
- [ ] Audit log (Track thay đổi)
- [ ] Notification khi có sửa đổi quan trọng

##### B. Xóa dự án
- [ ] **Permission check:**
  - [ ] Chỉ Admin mới được xóa
  - [ ] Popup cảnh báo permission nếu không phải Admin
- [ ] **Confirmation popup:**
  - [ ] Hiển thị tên dự án
  - [ ] Hiển thị số lượng Hồ sơ/Công việc sẽ bị xóa
  - [ ] Yêu cầu nhập tên dự án để confirm (Extra safety)
  - [ ] Checkbox "I understand this cannot be undone"
- [ ] **Cascade delete hoặc Archive:**
  - [ ] Option: Xóa vĩnh viễn (Hard delete)
  - [ ] Option: Lưu trữ (Soft delete - Recommended)
- [ ] **Impact check:**
  - [ ] Có công việc đang active không?
  - [ ] Có tài liệu được chia sẻ không?
  - [ ] Có task quá hạn chưa hoàn thành?
- [ ] Audit log
- [ ] Notification to stakeholders

**Số test case cần bổ sung:** ~12-15 (P1)

---

## 📈 ROADMAP BỔ SUNG TEST CASE

### Phase 1: CRITICAL (Week 1-2) - P0/P1

**Ưu tiên cao nhất - BLOCKER:**

1. **Tab Hồ sơ dự án** (50-60 TCs)
   - Tree view structure: 8 TCs
   - CRUD Thư mục/Tài liệu: 15 TCs
   - Upload + OCR: 8 TCs
   - Chi tiết tài liệu popup: 12 TCs
   - Version history: 5 TCs
   - Preview: 5 TCs
   - Download permission: 3 TCs
   - Re-organize (Drag & drop): 5 TCs
   - Sharing: 8 TCs
   - Export Excel: 3 TCs

2. **Tab Công việc** (25-30 TCs)
   - Danh sách + Highlight quá hạn: 5 TCs
   - Bộ lọc: 8 TCs
   - CRUD (Giao việc/Đặt hàng): 12 TCs
   - Bulk delete: 3 TCs
   - Tích hợp tiến độ: 5 TCs

3. **Tab Phân quyền** (20-25 TCs)
   - 4 Role types testing: 8 TCs
   - Add User/Unit logic: 8 TCs
   - ManageBy flag: 3 TCs
   - Edit/Delete permissions: 6 TCs

**Tổng Phase 1:** ~100-115 TCs

---

### Phase 2: HIGH Priority (Week 3) - P1

1. **Tab Thông tin & Tiến trình** (15-20 TCs)
   - QR Code: 5 TCs
   - Giai đoạn + Progress bar: 8 TCs
   - Metadata display: 4 TCs

2. **Edit/Delete Project** (12-15 TCs)
   - Edit flow: 8 TCs
   - Delete with confirmation: 5 TCs

3. **Danh sách dự án - Missing features** (8-10 TCs)
   - Sắp xếp: 3 TCs
   - Import: 4 TCs
   - View detail menu: 2 TCs

**Tổng Phase 2:** ~35-45 TCs

---

### Phase 3: MEDIUM Priority (Week 4) - P2

1. **Custom Fields** (8-10 TCs)
   - Dynamic fields: 4 TCs
   - Soft delete logic: 4 TCs

2. **Biểu mẫu nội bộ** (5-6 TCs)
   - Template selection: 3 TCs
   - Apply template: 2 TCs

3. **Performance & Advanced Non-functional** (8-10 TCs)
   - Load testing: 3 TCs
   - Stress testing: 2 TCs
   - Accessibility: 3 TCs

**Tổng Phase 3:** ~21-26 TCs

---

### Tổng hợp Roadmap

| Phase | Timeline | Priority | Số TCs | Tích lũy |
|-------|----------|----------|--------|----------|
| **Hiện tại** | - | - | 76 | 76 |
| **Phase 1** | Week 1-2 | P0/P1 | 100-115 | 176-191 |
| **Phase 2** | Week 3 | P1 | 35-45 | 211-236 |
| **Phase 3** | Week 4 | P2 | 21-26 | 232-262 |

**Tổng cộng dự kiến:** ~230-260 test cases để cover đầy đủ PRD

---

## 🎯 KHUYẾN NGHỊ

### 1. Hành động ngay lập tức (URGENT)

🔴 **STOP development nếu chưa có test case cho:**
- Tab Hồ sơ dự án (CORE feature)
- Tab Công việc (CORE feature)
- Tab Phân quyền (SECURITY critical)

### 2. Quy trình đề xuất

```
┌─────────────────────────────────────────────────────┐
│ WEEK 1-2: Focus on BLOCKER items                    │
├─────────────────────────────────────────────────────┤
│ • Tab Hồ sơ: Tree view + Upload + OCR (30 TCs)    │
│ • Tab Công việc: CRUD + Filter (20 TCs)            │
│ • Tab Phân quyền: Roles + Add/Edit (15 TCs)        │
│ • Daily: Write 15-20 TCs                            │
│ • Review: End of Week 1                             │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ WEEK 3: Complete critical features                  │
├─────────────────────────────────────────────────────┤
│ • Tab Hồ sơ: Version + Share + Export (20 TCs)     │
│ • Tab Tiến trình: QR + Progress (15 TCs)            │
│ • Edit/Delete flows (12 TCs)                        │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│ WEEK 4: Polish & Edge cases                         │
├─────────────────────────────────────────────────────┤
│ • Custom fields + Templates (10 TCs)                │
│ • Performance testing (10 TCs)                      │
│ • Final review & gap analysis                       │
└─────────────────────────────────────────────────────┘
```

### 3. Resource planning

| Role | Allocation | Tasks |
|------|------------|-------|
| **QA Lead** | 100% | - Review PRD<br>- Design test scenarios<br>- Approve test cases |
| **Senior Tester** | 100% | - Write Phase 1 TCs (50-60)<br>- Review junior's work |
| **Junior Tester 1** | 100% | - Write Phase 1 TCs (30-40)<br>- Execute basic functional TCs |
| **Junior Tester 2** | 50% | - Write Phase 2 TCs (20-25)<br>- Execute regression |

**Timeline:** 4 weeks từ ngày bắt đầu viết

### 4. Template chuẩn

Sử dụng format nhất quán cho tất cả test case:

```markdown
| ID | Module | Title | Pre-condition | Step | Test Data | Expected Result | Status | Priority | Create Date | Execute Date |
```

**Bắt buộc:**
- ID format: `TC-[TYPE]-[NUMBER]` (e.g., TC-FUNC-077, TC-SECU-078)
- Module: Tab/Section rõ ràng (e.g., "Tab Hồ sơ", "Tab Công việc")
- Priority: P0 (Blocker), P1 (High), P2 (Medium), P3 (Low)

### 5. Review checklist

Trước khi approve test case mới, check:

- [ ] Cover được yêu cầu PRD cụ thể nào?
- [ ] Có conflict với TC hiện tại không?
- [ ] Step rõ ràng, có thể reproduce?
- [ ] Expected result cụ thể, measurable?
- [ ] Priority hợp lý?
- [ ] Có test data mẫu (nếu cần)?

---

## 📋 PHẦN BỔ SUNG

### Test Case Template mẫu cho các feature thiếu

#### 1. Tab Hồ sơ - Tree View (Example)

```markdown
| ID | Module | Title | Pre-condition | Step | Test Data | Expected Result | Status | Priority |
|----|--------|-------|---------------|------|-----------|-----------------|--------|----------|
| TC-FUNC-077 | Tab Hồ sơ | Verify Tree Structure - Expand Node | - User has permission to view<br>- Tree has nested folders | 1. Navigate to Tab Hồ sơ<br>2. Click expand icon on folder "A" | Folder A has children: A.1, A.2 | Children displayed under parent<br>Expand icon changes to collapse | [ ] | P1 |
| TC-FUNC-078 | Tab Hồ sơ | Verify Tree Structure - Collapse Node | - Tree node is expanded | 1. Click collapse icon | - | Children hidden<br>Icon changes to expand | [ ] | P2 |
| TC-FUNC-079 | Tab Hồ sơ | Verify Search in Tree - Highlight Result | - Tree loaded<br>- Document "Hồ sơ A.1.2" exists | 1. Enter "A.1.2" in search box | - | - Result highlighted in yellow<br>- Tree auto-expands to show result<br>- Scroll to result | [ ] | P1 |
```

#### 2. Tab Hồ sơ - Upload & OCR (Example)

```markdown
| ID | Module | Title | Pre-condition | Step | Test Data | Expected Result | Status | Priority |
|----|--------|-------|---------------|------|-----------|-----------------|--------|----------|
| TC-FUNC-080 | Tab Hồ sơ | Verify Upload PDF - Success | - User has Input permission<br>- Document created | 1. Click Upload button<br>2. Select valid PDF file<br>3. Click Upload | file.pdf (2MB) | - Upload progress shown<br>- File saved<br>- Thumbnail generated | [ ] | P1 |
| TC-FUNC-081 | Tab Hồ sơ | Verify OCR - Processing Indicator | - Uploaded scanned PDF | 1. Upload triggers OCR | scanned.pdf | - Background color changes to YELLOW<br>- "Processing..." text shown<br>- Color reverts to default when done | [ ] | P0 |
| TC-FUNC-082 | Tab Hồ sơ | Verify OCR - Extract Text Success | - OCR processing completed | 1. Open document detail<br>2. View extracted text | - | - Text content extracted correctly<br>- Searchable PDF generated | [ ] | P1 |
| TC-VALI-083 | Tab Hồ sơ | Verify Upload - File Size Limit | - | 1. Select file > 50MB<br>2. Click Upload | large_file.pdf (60MB) | Error: "File size exceeds limit (50MB)" | [ ] | P2 |
```

#### 3. Tab Công việc - Deadline Highlight (Example)

```markdown
| ID | Module | Title | Pre-condition | Step | Test Data | Expected Result | Status | Priority |
|----|--------|-------|---------------|------|-----------|-----------------|--------|----------|
| TC-FUNC-084 | Tab Công việc | Verify Deadline Highlight - Overdue | - Task exists with deadline yesterday | 1. Navigate to Tab Công việc<br>2. View task list | Task deadline: 2026-02-09<br>Current date: 2026-02-10 | - Deadline cell background RED<br>- Tooltip: "Overdue by 1 day" | [ ] | P1 |
| TC-FUNC-085 | Tab Công việc | Verify Deadline Highlight - Due Today | - Task deadline is today | 1. View task list | Task deadline: 2026-02-10 (today) | - Deadline cell background ORANGE/YELLOW<br>- Tooltip: "Due today" | [ ] | P2 |
| TC-FUNC-086 | Tab Công việc | Verify Deadline Highlight - Upcoming | - Task deadline is tomorrow | 1. View task list | Task deadline: 2026-02-11 | No special highlight<br>Normal text color | [ ] | P2 |
```

---

## 🔍 PHÂN TÍCH THEO MODULE

### Coverage Matrix

| Module/Feature | PRD Section | Current TCs | Missing TCs | Priority | Coverage % |
|----------------|-------------|-------------|-------------|----------|------------|
| Danh sách dự án | 2 | 32 | 8 | P1 | 70% |
| Tab Thông tin & Tiến trình | 3.1 | 2 | 18 | P1 | 5% |
| **Tab Hồ sơ** | **3.2** | **1** | **60** | **P0** | **~2%** |
| **Tab Công việc** | **3.3** | **0** | **30** | **P0** | **0%** |
| **Tab Phân quyền** | **3.4** | **2** | **23** | **P1** | **10%** |
| Tạo dự án | 4 | 18 | 15 | P1 | 60% |
| Sửa/Xóa dự án | 5 | 1 | 14 | P1 | 20% |
| **TỔNG** | - | **76** | **~150** | - | **~35%** |

---

## ✍️ KẾT LUẬN

### Đánh giá chung

**Điểm mạnh:**
- ✅ Security testing rất đầy đủ (XSS, SQL injection, Command injection...)
- ✅ Browser compatibility & Responsive đã cover tốt
- ✅ Validation input cơ bản đầy đủ
- ✅ Business logic cho phần Filter & Permission assignment đã có

**Điểm yếu:**
- ❌ **CRITICAL:** 3 trong 4 tab chính (Hồ sơ, Công việc, Phân quyền) thiếu gần như hoàn toàn
- ❌ **CRITICAL:** Chức năng CORE nhất (Quản lý Hồ sơ Tree view) chỉ có ~2% coverage
- ❌ Upload + OCR feature hoàn toàn không được test
- ❌ Version history, Preview, Sharing - Không có test case
- ❌ Edit/Delete flows chưa đầy đủ

### Rủi ro

| Risk Level | Issue | Impact |
|------------|-------|--------|
| 🔴 **CRITICAL** | Tab Hồ sơ không được test | Data loss, Permission leak, OCR failures |
| 🔴 **CRITICAL** | Tab Công việc không được test | Sai tiến độ dự án, Deadline không alert |
| 🟠 **HIGH** | Tab Phân quyền thiếu | Security breach, Unauthorized access |
| 🟠 **HIGH** | Version history không test | Cannot rollback, Audit trail incomplete |
| 🟡 **MEDIUM** | QR Code không test | Feature không hoạt động |

### Hành động khuyến nghị

**IMMEDIATE (Trong 1 tuần):**
1. ✍️ Viết 50-60 test cases cho Tab Hồ sơ (Tree, Upload, OCR, Version, Share)
2. ✍️ Viết 25-30 test cases cho Tab Công việc
3. ✍️ Viết 20-25 test cases cho Tab Phân quyền
4. 🛑 BLOCK deployment cho đến khi Phase 1 hoàn thành

**SHORT-TERM (2-3 tuần):**
5. ✍️ Bổ sung Tab Thông tin & Tiến trình (15-20 TCs)
6. ✍️ Bổ sung Edit/Delete flows (12-15 TCs)
7. 🧪 Execute tất cả critical test cases
8. 📊 Report coverage lên 80%+

**LONG-TERM (1 tháng):**
9. ✍️ Hoàn thiện Custom fields, Templates
10. 🧪 Performance & Stress testing
11. 📚 Maintain test documentation
12. 🔄 Regression suite cho mỗi sprint

---

**Người lập:** QA Lead  
**Ngày:** 10/02/2026  
**Trạng thái:** ⚠️ URGENT - Cần hành động ngay

---

## 📎 PHỤ LỤC

### A. Danh sách test case ưu tiên cao cần viết ngay

#### Top 20 Critical Test Cases (Week 1)

1. TC-FUNC-077: Tree View - Expand/Collapse node
2. TC-FUNC-078: Tree View - Load large tree (1000+ nodes)
3. TC-FUNC-079: Tree View - Search and highlight
4. TC-FUNC-080: Upload file - Success (PDF, DOC, XLS)
5. TC-FUNC-081: Upload file - OCR processing indicator (Yellow background)
6. TC-FUNC-082: Upload file - OCR extract text success
7. TC-FUNC-083: Document detail - Version history display
8. TC-FUNC-084: Document detail - Preview PDF
9. TC-FUNC-085: Document detail - Download permission check
10. TC-FUNC-086: Share document - Add user with View permission
11. TC-FUNC-087: Share document - Add user with Download permission
12. TC-FUNC-088: Task list - Highlight overdue deadline (RED)
13. TC-FUNC-089: Task list - Filter by Status
14. TC-FUNC-090: Create task - Giao việc (Success)
15. TC-FUNC-091: Create task - Link to document
16. TC-FUNC-092: Delete task - Bulk delete with confirmation
17. TC-FUNC-093: Permissions - Add User with Manage role
18. TC-FUNC-094: Permissions - ManageBy flag prevents deletion
19. TC-FUNC-095: Permissions - Filter by Region/Area
20. TC-FUNC-096: Progress calculation - Auto-update when task complete

### B. Test Data Template

```yaml
# Sample Test Data for Document Upload
documents:
  - name: "Hồ sơ pháp lý A.1.pdf"
    type: "application/pdf"
    size: 2048576  # 2MB
    pages: 15
    ocr_required: true
    classification: "Tối mật"
    
  - name: "Báo cáo kỹ thuật.docx"
    type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    size: 512000  # 500KB
    ocr_required: false
    classification: "Mật"

# Sample Test Data for Tasks
tasks:
  - name: "Hoàn thiện hồ sơ pháp lý"
    code: "TASK-001"
    phase: "Đợt 1"
    priority: "Cao"
    assignee: "Nguyễn Văn A"
    deadline: "2026-02-15"
    status: "Đang thực hiện"
    progress: 60
    
  - name: "Thẩm định thiết kế"
    code: "TASK-002"
    phase: "Đợt 2"
    priority: "Trung bình"
    assignee: "Trần Thị B"
    deadline: "2026-02-09"  # Overdue
    status: "Chưa bắt đầu"
    progress: 0
```

### C. Automation Candidates

**High priority cho automation (Phase 2):**
- Tree view expand/collapse
- Search and filter combinations
- Upload file (Happy path)
- CRUD operations (Create/Read/Update/Delete)
- Permission checks
- Progress calculation

**Low priority cho automation:**
- OCR processing (Flaky, requires ML)
- Visual testing (Progress bars, Colors)
- Browser compatibility (Use Selenium Grid)

---

**END OF DOCUMENT**
