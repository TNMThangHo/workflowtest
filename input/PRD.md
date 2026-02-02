# PRD: Hệ thống Đăng nhập (Login System)

## 1. Giới thiệu

Tính năng đăng nhập cho phép người dùng truy cập vào hệ thống Admin Portal.

## 2. Yêu cầu chức năng

### 2.1. Form Đăng nhập

- Người dùng nhập Email và Password.
- Nút "Đăng nhập" (Login) chỉ active khi đã nhập đủ 2 trường.
- Có chức năng "Quên mật khẩu" (Forgot Password).

### 2.2. Validation

- **Email**: Phải đúng định dạng email (vd: user@example.com). Bắt buộc nhập.
- **Password**: Tối thiểu 6 ký tự. Bắt buộc nhập.

### 2.3. Quy trình xử lý

- **Thành công**: Email/Pass đúng -> Chuyển hướng vào Dashboard.
- **Thất bại**: Email/Pass sai -> Hiển thị thông báo lỗi "Thông tin đăng nhập không chính xác".
- **Khóa tài khoản**: Nếu nhập sai quá 5 lần, khóa tài khoản 15 phút.

## 3. Yêu cầu UI/UX (Tham chiếu Design)

- Màn hình căn giữa.
- Logo đặt phía trên cùng.
- Nút Login màu xanh dương (#007AFF).
- Input field có placeholder text màu xám nhạt.
