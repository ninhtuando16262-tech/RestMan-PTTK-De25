# HỆ THỐNG QUẢN LÝ NHÀ HÀNG RESTMAN (ĐỀ SỐ 25)
## BÀI TẬP LỚN MÔN PHÂN TÍCH THIẾT KẾ HỆ THỐNG THÔNG TIN (PTTK)

---

## 📌 1. TỔNG QUAN DỰ ÁN
Hệ thống **RestMan** được thiết kế nhằm phục vụ công tác quản lý và vận hành nhà hàng chuyên nghiệp với các tác nhân: **Khách hàng**, **Nhân viên quản lý**, **Nhân viên kho**, **Nhân viên bán hàng**.

Dự án này lập trình hoàn chỉnh **2 Module trọng tâm** theo đúng yêu cầu đề bài số 25, bám sát từng lớp giao diện (Boundary), điều khiển (Control), truy xuất dữ liệu (DAO/Repository) và thực thể (Entity) trong tài liệu đặc tả và file thiết kế:

1. **Module 1 – Khách hàng tìm kiếm thông tin món ăn:**
   - Luồng giao diện: `GDChinhKH` ➔ `GDThongTinMonAn` ➔ `GDThongTinChiTiet`.
   - Chức năng: Tìm kiếm theo từ khóa tên món, phân loại, mô tả; xem danh sách kết quả; xem chi tiết giá bán, khẩu phần, trạng thái phục vụ.
   - Xử lý ngoại lệ: Từ khóa rỗng hiển thị tất cả món ăn; từ khóa không khớp hiển thị thông báo *"Không tìm thấy món ăn phù hợp"*.
   - Phương thức DAO: `MonAnDAO.timKiemMonan(tuKhoa)`, `MonAnDAO.getChitietMonan(id)`.

2. **Module 2 – Thống kê nhà cung cấp theo số lượng hàng nhập:**
   - Luồng giao diện: `GDChinhQL` ➔ `GDChonThongKe` ➔ `GDTKNhaCungCap` ➔ `GDChiTietLanNhapNCC` ➔ `GDHoaDonNhap`.
   - Chức năng: Nhập khoảng ngày bắt đầu & kết thúc; thống kê tổng lượng hàng nhập từ các nhà cung cấp (sắp xếp giảm dần); xem danh sách các lần nhập/phiếu nhập của từng nhà cung cấp; xem chi tiết hóa đơn nhập từng nguyên liệu (số lượng, đơn giá, thành tiền, tổng tiền).
   - Xử lý ngoại lệ: Ngày bắt đầu > ngày kết thúc (hoặc để trống) báo lỗi *"Khoảng thời gian thống kê không hợp lệ"*; khoảng thời gian không có giao dịch báo *"Không có dữ liệu thống kê trong khoảng thời gian này"*.
   - Phương thức DAO: `TKnhacungcapDAO.getTKNhaCungCap(startDate, endDate)`, `HoaDonNhapDAO.getDSLanNhap(idNCC, startDate, endDate)`, `HoaDonNhapChiTietDAO.getChiTietHoaDonNhap(idHDNhap)`.

---

## 🚀 2. HƯỚNG DẪN KHỞI CHẠY WEB APP (1 CLICK)

### Cách 1: Chạy trực tiếp bằng file `run.bat` (Khuyên dùng)
- Nhấp đúp chuột vào file **`run.bat`** trong thư mục này.
- Hệ thống sẽ tự động khởi tạo cơ sở dữ liệu và mở trình duyệt tại địa chỉ: `http://localhost:8080`.

### Cách 2: Chạy bằng dòng lệnh Terminal
```bash
# 1. Khởi tạo cơ sở dữ liệu mẫu (nếu cần đặt lại dữ liệu ban đầu)
python database/init_db.py

# 2. Khởi chạy server và tự động mở trình duyệt
python run_browser.py
```
Hoặc chạy server trực tiếp:
```bash
python app.py
```
Sau đó truy cập: [http://localhost:8080](http://localhost:8080) trên trình duyệt web.

---

## 🔑 3. TÀI KHOẢN ĐĂNG NHẬP HỆ THỐNG
Trang đăng nhập có sẵn tính năng **"Đăng nhập nhanh 1-Click"** theo vai trò để thuận tiện nhất cho việc chấm bài và demo:

| Vai trò | Tên đăng nhập | Mật khẩu | Họ và tên | Chức năng chính |
| :--- | :--- | :--- | :--- | :--- |
| **Khách hàng** | `khachhang1` | `123456` | Nguyễn Văn An | **Module 1**: Tìm kiếm & xem chi tiết món ăn |
| **Nhân viên quản lý** | `quanly1` | `123456` | Trần Thị Mai | **Module 2**: Xem báo cáo thống kê NCC theo lượng nhập |
| **Nhân viên kho** | `nhanvienkho1` | `123456` | Lê Hoàng Nam | Quản lý nhập nguyên liệu |
| **Nhân viên bán hàng** | `nhanvienbanhang1` | `123456` | Phạm Thu Hà | Phục vụ bàn & thanh toán |

---

## 📂 4. CẤU TRÚC THƯ MỤC DỰ ÁN
```
PTTK/
├── app.py                          # Web Server chính (Starlette + Jinja2 + SQLite)
├── run.bat                         # File chạy tự động 1-click trên Windows
├── run_browser.py                  # Script khởi chạy và tự mở trình duyệt web
├── README.md                       # Tài liệu hướng dẫn sử dụng và giới thiệu
│
├── database/                       # Tầng Cơ Sở Dữ Liệu
│   ├── restman.db                  # Database SQLite có sẵn dữ liệu mẫu thực tế
│   ├── init_db.py                  # Script tái tạo và nạp dữ liệu mẫu
│   └── schema.sql                  # Toàn bộ mã DDL SQL thiết kế 16 bảng CSDL
│
├── models/                         # Tầng Thực thể (Entity) & Truy xuất CSDL (DAO)
│   ├── entities.py                 # Các lớp Thanhvien, Khachhang, Nhanvien, Monan, Nhacungcap, Hoadonnhap, TKnhacungcap...
│   └── dao.py                      # Các lớp MonAnDAO, TKnhacungcapDAO, HoaDonNhapDAO, HoaDonNhapChiTietDAO, ThanhVienDAO
│
├── templates/                      # Tầng Giao diện (Boundary) bám sát đặc tả PTTK
│   ├── base.html                   # Giao diện khung chuẩn, responsive Bootstrap 5
│   ├── login.html                  # Giao diện đăng nhập & chọn vai trò
│   ├── gd_chinh_kh.html            # Lớp GDChinhKH (Trang chủ khách hàng, bám sát Wireframe)
│   ├── gd_thong_tin_mon_an.html    # Lớp GDThongTinMonAn (Tìm kiếm món ăn, danh sách kết quả)
│   ├── gd_thong_tin_chi_tiet.html  # Lớp GDThongTinChiTiet (Chi tiết món ăn)
│   ├── gd_chinh_ql.html            # Lớp GDChinhQL (Bàn làm việc quản lý)
│   ├── gd_chon_thong_ke.html       # Lớp GDChonThongKe (Chọn loại báo cáo thống kê)
│   ├── gd_tk_nha_cung_cap.html     # Lớp GDTKNhaCungCap (Thống kê NCC theo lượng nhập)
│   ├── gd_chi_tiet_lan_nhap.html   # Lớp GDChiTietLanNhapNCC (Lịch sử các lần nhập của NCC)
│   └── gd_hoa_don_nhap.html        # Lớp GDHoaDonNhap (Hóa đơn nhập và chi tiết nguyên liệu)
│
├── static/                         # Tài nguyên tĩnh
│   ├── css/style.css               # CSS phong cách nhà hàng sang trọng, hiện đại
│   └── js/main.js                  # Script tương tác người dùng
│
├── tests/                          # Tầng Kiểm thử Đơn vị (Unit Test)
│   └── test_dao.py                 # 12 bài test tự động cho toàn bộ phương thức DAO & ngoại lệ
│
└── java_src/                       # Bộ mã nguồn Java thuần (Theo chuẩn Java Web MVC PTIT)
    ├── model/                      # Các POJO Entity chuẩn Java (ThanhVien, MonAn, TKnhacungcap...)
    └── dao/                        # Các lớp DAO chuẩn JDBC (MonAnDAO, TKnhacungcapDAO, HoaDonNhapDAO...)
```

---

## 🧪 5. KIỂM THỬ ĐƠN VỊ (UNIT TEST)
Để kiểm tra tính đúng đắn của toàn bộ các phương thức DAO và việc xử lý các trường hợp ngoại lệ:
```bash
python -m unittest tests/test_dao.py
```
**Kết quả kiểm thử:**
- `test_timKiemMonan_all_when_empty_keyword`: ✅ PASSED (Hiển thị toàn bộ khi từ khóa rỗng)
- `test_timKiemMonan_found`: ✅ PASSED (Tìm kiếm có kết quả)
- `test_timKiemMonan_not_found`: ✅ PASSED (Xử lý khi không có món ăn phù hợp)
- `test_getChitietMonan`: ✅ PASSED (Lấy chi tiết món ăn)
- `test_getTKNhaCungCap_valid`: ✅ PASSED (Thống kê theo lượng nhập giảm dần)
- `test_getTKNhaCungCap_invalid_date_range`: ✅ PASSED (Bắt lỗi ngày BĐ > ngày KT)
- `test_getTKNhaCungCap_empty_date`: ✅ PASSED (Bắt lỗi bỏ trống thời gian)
- `test_getTKNhaCungCap_no_data`: ✅ PASSED (Xử lý khi không có phát sinh giao dịch)
- `test_getDSLanNhap`: ✅ PASSED (Lấy danh sách các lần nhập của NCC)
- `test_getChiTietHoaDonNhap`: ✅ PASSED (Lấy chi tiết hóa đơn và từng nguyên liệu)
- `test_kiemTraDangNhap_success` & `test_kiemTraDangNhap_fail`: ✅ PASSED (Xác thực đăng nhập)

Tất cả **12/12 test case** chạy thành công trong 0.02s!
