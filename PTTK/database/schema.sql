-- ====================================================================
-- DATABASE SCHEMA: HỆ THỐNG QUẢN LÝ NHÀ HÀNG RESTMAN (ĐỀ SỐ 25)
-- Dành cho đồ án môn Phân Tích Thiết Kế Hệ Thống Thông Tin (PTTK)
-- ====================================================================

-- 1. Bảng Thành viên (Tài khoản người dùng trong hệ thống)
CREATE TABLE IF NOT EXISTS tbl_thanhvien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT NOT NULL,
    tendangnhap TEXT UNIQUE NOT NULL,
    matkhau TEXT NOT NULL,
    ngaysinh TEXT,
    diachi TEXT,
    email TEXT,
    sdt TEXT,
    vaitro TEXT NOT NULL CHECK (vaitro IN ('QuanLy', 'NhanVienKho', 'NhanVienBanHang', 'KhachHang'))
);

-- 2. Bảng Nhân viên (Kế thừa từ Thành viên)
CREATE TABLE IF NOT EXISTS tbl_nhanvien (
    id INTEGER PRIMARY KEY,
    vitricongviec TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES tbl_thanhvien(id) ON DELETE CASCADE
);

-- 3. Bảng Khách hàng (Kế thừa từ Thành viên)
CREATE TABLE IF NOT EXISTS tbl_khachhang (
    id INTEGER PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES tbl_thanhvien(id) ON DELETE CASCADE
);

-- 4. Bảng Thẻ thành viên
CREATE TABLE IF NOT EXISTS tbl_the (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mathe TEXT UNIQUE NOT NULL,
    id_khachhang INTEGER NOT NULL UNIQUE,
    hangthe TEXT DEFAULT 'Thường',
    ngaytao TEXT NOT NULL,
    diemtichluy INTEGER DEFAULT 0,
    FOREIGN KEY (id_khachhang) REFERENCES tbl_khachhang(id) ON DELETE CASCADE
);

-- 5. Bảng Món ăn (Phục vụ Module Tìm kiếm thông tin món ăn)
CREATE TABLE IF NOT EXISTS tbl_monan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mamon TEXT UNIQUE NOT NULL,
    tenmon TEXT NOT NULL,
    loai TEXT NOT NULL,
    khauphan TEXT NOT NULL,
    giatien REAL NOT NULL,
    mota TEXT,
    hinhanh TEXT,
    trangthai TEXT DEFAULT 'Đang phục vụ'
);

-- 6. Bảng Nguyên liệu
CREATE TABLE IF NOT EXISTS tbl_nguyenlieu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manguyenlieu TEXT UNIQUE NOT NULL,
    tennguyenlieu TEXT NOT NULL,
    phanloai TEXT NOT NULL,
    soluongton REAL NOT NULL DEFAULT 0,
    donvitinh TEXT NOT NULL,
    dongia REAL NOT NULL,
    hansudung TEXT
);

-- 7. Bảng Nhà cung cấp (Phục vụ Module Thống kê nhà cung cấp theo lượng nhập)
CREATE TABLE IF NOT EXISTS tbl_nhacungcap (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manhacungcap TEXT UNIQUE NOT NULL,
    ten TEXT NOT NULL,
    diachi TEXT NOT NULL,
    sdt TEXT NOT NULL,
    email TEXT NOT NULL,
    mota TEXT
);

-- 8. Bảng Hóa đơn nhập hàng (Phiếu nhập nguyên liệu)
CREATE TABLE IF NOT EXISTS tbl_hoadonnhap (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mahoadonnhap TEXT UNIQUE NOT NULL,
    ngaynhap TEXT NOT NULL,
    id_nhacungcap INTEGER NOT NULL,
    id_nhanvienkho INTEGER NOT NULL,
    tongtien REAL NOT NULL DEFAULT 0,
    ghichu TEXT,
    FOREIGN KEY (id_nhacungcap) REFERENCES tbl_nhacungcap(id) ON DELETE CASCADE,
    FOREIGN KEY (id_nhanvienkho) REFERENCES tbl_thanhvien(id)
);

-- 9. Bảng Chi tiết hóa đơn nhập hàng
CREATE TABLE IF NOT EXISTS tbl_hoadonnhapchitiet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_hoadonnhap INTEGER NOT NULL,
    id_nguyenlieu INTEGER NOT NULL,
    soluong REAL NOT NULL,
    dongianhap REAL NOT NULL,
    thanhtien REAL NOT NULL,
    FOREIGN KEY (id_hoadonnhap) REFERENCES tbl_hoadonnhap(id) ON DELETE CASCADE,
    FOREIGN KEY (id_nguyenlieu) REFERENCES tbl_nguyenlieu(id)
);

-- 10. Bảng Bàn ăn
CREATE TABLE IF NOT EXISTS tbl_ban (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maban TEXT UNIQUE NOT NULL,
    soban INTEGER NOT NULL,
    tinhtrang TEXT DEFAULT 'Trống',
    giodat TEXT
);

-- 11. Bảng Combo
CREATE TABLE IF NOT EXISTS tbl_combo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    macombo TEXT UNIQUE NOT NULL,
    tencombo TEXT NOT NULL,
    mota TEXT,
    giatien REAL NOT NULL
);

-- 12. Bảng Chi tiết Combo (Combo chứa các món ăn nào)
CREATE TABLE IF NOT EXISTS tbl_cbchitiet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_combo INTEGER NOT NULL,
    id_monan INTEGER NOT NULL,
    soluong INTEGER DEFAULT 1,
    FOREIGN KEY (id_combo) REFERENCES tbl_combo(id) ON DELETE CASCADE,
    FOREIGN KEY (id_monan) REFERENCES tbl_monan(id) ON DELETE CASCADE
);

-- 13. Bảng Đơn đặt (Đặt bàn / đặt món)
CREATE TABLE IF NOT EXISTS tbl_dondat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    madon TEXT UNIQUE NOT NULL,
    id_khachhang INTEGER NOT NULL,
    id_ban INTEGER,
    ngaydat TEXT NOT NULL,
    giodat TEXT NOT NULL,
    trangthai TEXT DEFAULT 'Chờ xác nhận',
    FOREIGN KEY (id_khachhang) REFERENCES tbl_khachhang(id),
    FOREIGN KEY (id_ban) REFERENCES tbl_ban(id)
);

-- 14. Bảng Món ăn gọi trong đơn đặt
CREATE TABLE IF NOT EXISTS tbl_monangoi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_dondat INTEGER NOT NULL,
    id_monan INTEGER NOT NULL,
    soluong INTEGER DEFAULT 1,
    FOREIGN KEY (id_dondat) REFERENCES tbl_dondat(id) ON DELETE CASCADE,
    FOREIGN KEY (id_monan) REFERENCES tbl_monan(id)
);

-- 15. Bảng Combo gọi trong đơn đặt
CREATE TABLE IF NOT EXISTS tbl_combogoi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_dondat INTEGER NOT NULL,
    id_combo INTEGER NOT NULL,
    soluong INTEGER DEFAULT 1,
    FOREIGN KEY (id_dondat) REFERENCES tbl_dondat(id) ON DELETE CASCADE,
    FOREIGN KEY (id_combo) REFERENCES tbl_combo(id)
);

-- 16. Bảng Hóa đơn bán hàng
CREATE TABLE IF NOT EXISTS tbl_hoadon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mahoadon TEXT UNIQUE NOT NULL,
    id_khachhang INTEGER NOT NULL,
    id_nhanvienbanhang INTEGER NOT NULL,
    id_dondat INTEGER NOT NULL,
    ngayxuat TEXT NOT NULL,
    tongtien REAL NOT NULL DEFAULT 0,
    tinhtrang TEXT DEFAULT 'Chưa thanh toán',
    FOREIGN KEY (id_khachhang) REFERENCES tbl_khachhang(id),
    FOREIGN KEY (id_nhanvienbanhang) REFERENCES tbl_thanhvien(id),
    FOREIGN KEY (id_dondat) REFERENCES tbl_dondat(id)
);
