# PRD: Chức năng Đăng ký Tài khoản (User Registration)

| Mục                 | Chi tiết                     |
| :------------------ | :--------------------------- |
| **Dự án**           | [Tên Dự Án Của Bạn]          |
| **Phiên bản**       | 1.0                          |
| **Trạng thái**      | Draft / In-Review / Approved |
| **Ngày tạo**        | 30/01/2026                   |
| **Người thực hiện** | [Tên Bạn]                    |

---

## 1. Tổng quan (Overview)

### 1.1. Mục tiêu (Objective)

Cho phép người dùng mới tạo tài khoản cá nhân trên hệ thống để truy cập vào các tính năng dành riêng cho thành viên.

### 1.2. Phạm vi (Scope)

- **Trong phạm vi (In-scope):**
  - Đăng ký bằng Email và Mật khẩu.
  - Validation (kiểm tra dữ liệu) tại Client-side và Server-side.
  - Gửi email xác thực (OTP hoặc Link kích hoạt).
- **Ngoài phạm vi (Out-scope) - (Dành cho Phase 2):**
  - Đăng ký bằng Google/Facebook (Social Login).
  - Đăng ký bằng số điện thoại.

---

## 2. User Stories

| ID        | Story                                                                           | Tiêu chí chấp nhận (Acceptance Criteria)                                                                                   |
| :-------- | :------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------- |
| **US-01** | Là một**khách (guest)**, tôi muốn **đăng ký tài khoản** để **sử dụng dịch vụ**. | 1. Đăng ký thành công với thông tin hợp lệ.`<br>`2. Nhận được thông báo thành công.`<br>`3. Dữ liệu được lưu vào Database. |
| **US-02** | Là một**hệ thống**, tôi muốn **xác thực email** để **ngăn chặn spam**.          | 1. Gửi email xác thực ngay sau khi submit form.`<br>`2. Tài khoản ở trạng thái "Pending" cho đến khi xác thực.             |

---

## 3. Yêu cầu Chức năng (Functional Requirements)

### 3.1. Giao diện người dùng (UI Components)

Màn hình Đăng ký bao gồm các trường sau:

1. **Họ và tên:** Input text.
2. **Email:** Input text.
3. **Mật khẩu:** Input password (có icon "con mắt" để hiện/ẩn).
4. **Nhập lại mật khẩu:** Input password.
5. **Checkbox:** "Tôi đồng ý với Điều khoản sử dụng".
6. **Nút CTA:** "Đăng ký" (Button).
7. **Link điều hướng:** "Đã có tài khoản? Đăng nhập ngay".

### 3.2. Quy tắc Validation (Data Dictionary & Rules)

| Tên trường      | Kiểu dữ liệu | Bắt buộc? | Quy tắc Validate & Thông báo lỗi (Error Message)                                                                                                              |
| :-------------- | :----------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Họ và tên**   | String       | Có        | - Không được để trống.`<br>` - Tối thiểu 2 ký tự. `<br>` - Không chứa ký tự đặc biệt/số.                                                                      |
| **Email**       | String       | Có        | - Đúng định dạng email (regex standard).`<br>` - **Duy nhất:** Không trùng với email đã tồn tại trong hệ thống. `<br>` -> Lỗi: _"Email này đã được sử dụng."_ |
| **Mật khẩu**    | String       | Có        | - Tối thiểu 8 ký tự.`<br>` - Phải bao gồm: 1 chữ hoa, 1 chữ thường, 1 số, 1 ký tự đặc biệt. `<br>` -> Lỗi: _"Mật khẩu chưa đủ mạnh."_                         |
| **Nhập lại MK** | String       | Có        | - Phải trùng khớp với trường Mật khẩu.`<br>` -> Lỗi: _"Mật khẩu nhập lại không khớp."_                                                                        |
| **Điều khoản**  | Boolean      | Có        | - Bắt buộc phải tick chọn.                                                                                                                                    |

### 3.3. Luồng xử lý (Logic Flow)

1. User truy cập trang Đăng ký.
2. User nhập thông tin và nhấn nút "Đăng ký".
3. **Client-side Validation:** Hệ thống kiểm tra format dữ liệu.
   - Nếu sai: Hiển thị lỗi màu đỏ ngay dưới trường tương ứng.
   - Nếu đúng: Gửi request API lên Server.
4. **Server-side Validation:**
   - Kiểm tra email đã tồn tại chưa.
   - Kiểm tra tính toàn vẹn dữ liệu.
5. **Xử lý kết quả:**
   - **Thành công (201 Created):**
     - Tạo bản ghi user mới trong DB (trạng thái: `unverified`).
     - Mã hóa mật khẩu (Hashing).
     - Gửi email chứa Link/OTP xác thực.
     - Chuyển hướng user sang trang "Vui lòng kiểm tra email".
   - **Thất bại (400 Bad Request / 500 Error):**
     - Hiển thị thông báo lỗi cụ thể từ server trả về (Toast message hoặc Alert).

---

## 4. Yêu cầu Phi chức năng (Non-Functional Requirements)

### 4.1. Bảo mật (Security)

- Mật khẩu **TUYỆT ĐỐI KHÔNG** được lưu dưới dạng plain-text. Phải được hash (sử dụng bcrypt hoặc Argon2).
- API đăng ký phải có cơ chế Rate Limiting (giới hạn số lần request) để chống spam/brute-force (ví dụ: tối đa 5 request/phút từ 1 IP).
- Giao thức truyền tải: HTTPS.

### 4.2. Hiệu năng (Performance)

- Thời gian phản hồi API đăng ký: < 5 giây.
- Email xác thực phải được gửi đi trong vòng 10 giây sau khi đăng ký.

### 4.3. Tương thích (Compatibility)

- Hoạt động tốt trên các trình duyệt: Chrome, Firefox, Safari, Edge, Operamini
- Responsive trên Mobile, Tablet, Desktop.

---

## 5. Analytics & Tracking

- Track sự kiện: `click_signup_button`.
- Track sự kiện: `signup_success`.
- Track sự kiện: `signup_failed` (kèm theo lý do lỗi để monitor).

---

## 6. Tài liệu tham khảo & Mockup

- Link Design: https://stitch.withgoogle.com/projects/17188758224360973428
- Link API Swagger: [Chèn link tại đây]
