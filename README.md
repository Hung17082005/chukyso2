Giới thiệu

Đây là một hệ thống mô phỏng việc gửi và nhận file có kèm chữ ký số RSA** giữa hai thực thể: Người gửi và Người nhận.  
Hệ thống hoạt động trên giao diện web, đảm bảo người nhận có thể:
- Xác minh tính toàn vẹn và tính xác thực** của file
- Tải xuống file gốc và file chữ ký** ngay trên ứng dụng

---
![image](https://github.com/user-attachments/assets/06b48fdc-5c48-492a-ba9b-fc3f998e07c3)

Chức năng

Người Gửi
- Tải lên file cần gửi
- Tự động ký số bằng khóa RSA riêng
- Gửi file gốc, chữ ký và public key tới người nhận qua HTTP

 Người Nhận
- Tự động nhận file (gốc, chữ ký, public key)
- Hiển thị danh sách file đã nhận
- Tải file gốc và chữ ký xuống
- Thực hiện xác minh chữ ký số trong ứng dụng

---

Cách thức hoạt động

1. **Người gửi** chọn file → hệ thống tạo chữ ký RSA → lưu file `.sig` và `public.pem`
2. Người gửi nhấn “Gửi” → hệ thống POST 3 file (gốc, chữ ký, public key) đến server người nhận
3. **Người nhận** tự động lưu các file vào `inbox/` và hiển thị lên giao diện
4. Người nhận chọn file và nhấn “Xác minh” để hệ thống kiểm tra chữ ký:
   - ✅ Hợp lệ: chữ ký đúng và file không bị thay đổi
   - ❌ Không hợp lệ: file bị thay đổi hoặc chữ ký sai

Công nghệ sử dụng

Thành phần       Mô tả                                      

 Python           Ngôn ngữ chính                             
 Flask            Framework web nhẹ để tạo API và giao diện 
 PyCryptodome     Thư viện mã hóa RSA, ký và xác minh       
 HTML + CSS       Tạo giao diện cho người gửi & nhận        
 Bootstrap/CSS    Tùy chỉnh giao diện (nếu nâng cấp thêm)   
 REST API (POST)  Gửi file qua HTTP giữa 2 app               

![image](https://github.com/user-attachments/assets/59e73d14-b8b6-4503-9641-d1550e32f8e5)

## 🚀 Cách chạy hệ thống

1. **Cài thư viện**:

```bash
pip install flask pycryptodome
