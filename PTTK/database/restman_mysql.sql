-- ====================================================================
-- DATABASE MYSQL: HỆ THỐNG QUẢN LÝ NHÀ HÀNG RESTMAN (ĐỀ SỐ 25)
-- Dành cho môn Phân Tích Thiết Kế Hệ Thống Thông Tin (PTTK)
-- Tương thích: MySQL 5.7 / 8.0 / MariaDB / XAMPP phpMyAdmin
-- ====================================================================

CREATE DATABASE IF NOT EXISTS `restman` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `restman`;

-- 1. Bảng Thành viên
DROP TABLE IF EXISTS `tbl_hoadonnhapchitiet`;
DROP TABLE IF EXISTS `tbl_hoadonnhap`;
DROP TABLE IF EXISTS `tbl_hoadon`;
DROP TABLE IF EXISTS `tbl_monangoi`;
DROP TABLE IF EXISTS `tbl_combogoi`;
DROP TABLE IF EXISTS `tbl_cbchitiet`;
DROP TABLE IF EXISTS `tbl_dondat`;
DROP TABLE IF EXISTS `tbl_the`;
DROP TABLE IF EXISTS `tbl_khachhang`;
DROP TABLE IF EXISTS `tbl_nhanvien`;
DROP TABLE IF EXISTS `tbl_thanhvien`;
DROP TABLE IF EXISTS `tbl_monan`;
DROP TABLE IF EXISTS `tbl_nguyenlieu`;
DROP TABLE IF EXISTS `tbl_nhacungcap`;
DROP TABLE IF EXISTS `tbl_ban`;
DROP TABLE IF EXISTS `tbl_combo`;

CREATE TABLE `tbl_thanhvien` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ten` VARCHAR(100) NOT NULL,
    `tendangnhap` VARCHAR(50) NOT NULL UNIQUE,
    `matkhau` VARCHAR(100) NOT NULL,
    `ngaysinh` DATE,
    `diachi` VARCHAR(255),
    `email` VARCHAR(100),
    `sdt` VARCHAR(20),
    `vaitro` VARCHAR(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Bảng Nhân viên
CREATE TABLE `tbl_nhanvien` (
    `id` INT PRIMARY KEY,
    `vitricongviec` VARCHAR(100) NOT NULL,
    FOREIGN KEY (`id`) REFERENCES `tbl_thanhvien`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Bảng Khách hàng
CREATE TABLE `tbl_khachhang` (
    `id` INT PRIMARY KEY,
    FOREIGN KEY (`id`) REFERENCES `tbl_thanhvien`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Bảng Thẻ thành viên
CREATE TABLE `tbl_the` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `mathe` VARCHAR(50) NOT NULL UNIQUE,
    `id_khachhang` INT NOT NULL UNIQUE,
    `hangthe` VARCHAR(50) DEFAULT 'Thường',
    `ngaytao` DATE NOT NULL,
    `diemtichluy` INT DEFAULT 0,
    FOREIGN KEY (`id_khachhang`) REFERENCES `tbl_khachhang`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Bảng Món ăn
CREATE TABLE `tbl_monan` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `mamon` VARCHAR(20) NOT NULL UNIQUE,
    `tenmon` VARCHAR(150) NOT NULL,
    `loai` VARCHAR(50) NOT NULL,
    `khauphan` VARCHAR(50) NOT NULL,
    `giatien` DOUBLE NOT NULL,
    `mota` TEXT,
    `hinhanh` VARCHAR(255),
    `trangthai` VARCHAR(50) DEFAULT 'Đang phục vụ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Bảng Nguyên liệu
CREATE TABLE `tbl_nguyenlieu` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `manguyenlieu` VARCHAR(20) NOT NULL UNIQUE,
    `tennguyenlieu` VARCHAR(150) NOT NULL,
    `phanloai` VARCHAR(50) NOT NULL,
    `soluongton` DOUBLE NOT NULL DEFAULT 0,
    `donvitinh` VARCHAR(20) NOT NULL,
    `dongia` DOUBLE NOT NULL,
    `hansudung` DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Bảng Nhà cung cấp
CREATE TABLE `tbl_nhacungcap` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `manhacungcap` VARCHAR(20) NOT NULL UNIQUE,
    `ten` VARCHAR(150) NOT NULL,
    `diachi` VARCHAR(255) NOT NULL,
    `sdt` VARCHAR(20) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `mota` TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Bảng Hóa đơn nhập hàng
CREATE TABLE `tbl_hoadonnhap` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `mahoadonnhap` VARCHAR(50) NOT NULL UNIQUE,
    `ngaynhap` DATE NOT NULL,
    `id_nhacungcap` INT NOT NULL,
    `id_nhanvienkho` INT NOT NULL,
    `tongtien` DOUBLE NOT NULL DEFAULT 0,
    `ghichu` TEXT,
    FOREIGN KEY (`id_nhacungcap`) REFERENCES `tbl_nhacungcap`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`id_nhanvienkho`) REFERENCES `tbl_thanhvien`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Bảng Chi tiết hóa đơn nhập hàng
CREATE TABLE `tbl_hoadonnhapchitiet` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `id_hoadonnhap` INT NOT NULL,
    `id_nguyenlieu` INT NOT NULL,
    `soluong` DOUBLE NOT NULL,
    `dongianhap` DOUBLE NOT NULL,
    `thanhtien` DOUBLE NOT NULL,
    FOREIGN KEY (`id_hoadonnhap`) REFERENCES `tbl_hoadonnhap`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`id_nguyenlieu`) REFERENCES `tbl_nguyenlieu`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==================== CHÈN DỮ LIỆU MẪU ====================

INSERT INTO `tbl_thanhvien` (`id`, `ten`, `tendangnhap`, `matkhau`, `ngaysinh`, `diachi`, `email`, `sdt`, `vaitro`) VALUES
(1, 'Nguyễn Văn An', 'khachhang1', '123456', '1998-05-15', '128 Cầu Giấy, Hà Nội', 'an.nv@gmail.com', '0912345678', 'KhachHang'),
(2, 'Trần Thị Mai', 'quanly1', '123456', '1988-10-20', '45 Hoàng Hoa Thám, Ba Đình, Hà Nội', 'mai.tt@restman.vn', '0987654321', 'QuanLy'),
(3, 'Lê Hoàng Nam', 'nhanvienkho1', '123456', '1995-03-12', '88 Trần Phú, Hà Đông, Hà Nội', 'nam.lh@restman.vn', '0933445566', 'NhanVienKho'),
(4, 'Phạm Thu Hà', 'nhanvienbanhang1', '123456', '2001-08-25', '15 Chùa Bộc, Đống Đa, Hà Nội', 'ha.pt@restman.vn', '0977889900', 'NhanVienBanHang');

INSERT INTO `tbl_nhanvien` (`id`, `vitricongviec`) VALUES
(2, 'Quản lý vận hành'),
(3, 'Thủ kho thực phẩm'),
(4, 'Nhân viên phục vụ/bán hàng');

INSERT INTO `tbl_khachhang` (`id`) VALUES (1);

INSERT INTO `tbl_the` (`id`, `mathe`, `id_khachhang`, `hangthe`, `ngaytao`, `diemtichluy`) VALUES
(1, 'THE-VIP-001', 1, 'Vàng', '2026-01-10', 350);

INSERT INTO `tbl_monan` (`id`, `mamon`, `tenmon`, `loai`, `khauphan`, `giatien`, `mota`, `hinhanh`, `trangthai`) VALUES
(1, 'MA01', 'Phở bò tái gầu đặc biệt', 'Món chính', '1 người', 65000, 'Bò tái tươi ngon kết hợp cùng gầu giòn thơm ngon hảo hạng.', '', 'Đang phục vụ'),
(2, 'MA02', 'Bún chả Hà Nội truyền thống', 'Món chính', '1 người', 55000, 'Chả miếng và chả băm nướng than hoa thơm lừng ăn kèm nem rán.', '', 'Đang phục vụ'),
(3, 'MA03', 'Bò bít tết sốt tiêu đen', 'Món chính', '1-2 người', 135000, 'Thịt thăn bò tươi nhập khẩu nướng mềm mọng, đậm đà với sốt tiêu đen.', '', 'Đang phục vụ'),
(4, 'MA04', 'Lẩu hải sản chua cay thập cẩm', 'Món lẩu', '3-4 người', 380000, 'Nước lẩu Tomyum đậm đà kết hợp tôm sú, mực lá, nghêu, cá hồi.', '', 'Đang phục vụ'),
(5, 'MA05', 'Nem hải sản chiên xù', 'Khai vị', '2-4 người', 75000, 'Vỏ nem giòn rụm bọc nhân tôm mực ngọt thịt kết hợp sốt mayonnaise.', '', 'Đang phục vụ'),
(6, 'MA06', 'Cá hồi áp chảo sốt chanh leo', 'Món chính', '1 người', 185000, 'Cá hồi Nauy áp chảo da giòn thịt ngọt mềm, phủ sốt chanh leo chua thanh.', '', 'Đang phục vụ'),
(7, 'MA07', 'Gà nướng mật ong Tây Bắc', 'Món nướng', '2-3 người', 220000, 'Gà ri thả vườn tẩm ướp hạt dổi mắc khén nướng than hồng.', '', 'Đang phục vụ'),
(8, 'MA08', 'Salad cá ngừ rau củ', 'Khai vị', '1-2 người', 68000, 'Cá ngừ đại dương trộn cùng xà lách, cà chua bi, trứng luộc.', '', 'Đang phục vụ'),
(9, 'MA09', 'Mực một nắng nướng sa tế', 'Món nướng', '2-3 người', 160000, 'Mực một nắng Phú Quốc nướng giòn ngọt cay nồng.', '', 'Đang phục vụ'),
(10, 'MA10', 'Cơm chiên hải sản hoàng bào', 'Món chính', '1-2 người', 85000, 'Hạt cơm dẻo vàng óng bọc trứng mềm mịn kết hợp tôm, mực giòn ngọt.', '', 'Đang phục vụ'),
(11, 'MA11', 'Trà đào cam sả', 'Đồ uống', '1 người', 38000, 'Trà đào thanh mát quyện cùng cam tươi mọng nước, sả thơm.', '', 'Đang phục vụ'),
(12, 'MA12', 'Chè sen long nhãn', 'Tráng miệng', '1 người', 32000, 'Hạt sen bùi béo trong cùi nhãn ngọt giòn thanh khiết.', '', 'Đang phục vụ');

INSERT INTO `tbl_nhacungcap` (`id`, `manhacungcap`, `ten`, `diachi`, `sdt`, `email`, `mota`) VALUES
(1, 'NCC01', 'Công ty TNHH Thực phẩm Sạch Ba Vì', 'Xã Vân Hòa, Ba Vì, Hà Nội', '02433889911', 'bavifarm@cleanfood.vn', 'Cung cấp thịt bò tươi, thịt heo đạt chuẩn VietGAP'),
(2, 'NCC02', 'Nông trại Rau Hữu cơ Đà Lạt EcoFarm', 'Phường 7, TP. Đà Lạt, Lâm Đồng', '02633778899', 'contact@dalatecofarm.vn', 'Chuyên cung cấp rau củ quả tươi, xà lách, nấm sạch'),
(3, 'NCC03', 'Hải sản Tươi sống Biển Đông', 'Số 98 Cảng Cát Lái, Hải Phòng', '02253667788', 'kinhdoanh@biendongseafood.com', 'Cung cấp hải sản tôm sú tươi, cá hồi Nauy, mực một nắng'),
(4, 'NCC04', 'Tổng kho Nông sản & Gia vị Việt Hà', 'Lô B3 KCN Tiên Sơn, Bắc Ninh', '02223556677', 'vietha.spices@gmail.com', 'Phân phối gia vị đóng hộp, nước mắm truyền thống, gạo ST25'),
(5, 'NCC05', 'Công ty Đồ uống & Nước giải khát Thủ Đô', 'Km 10 Quốc lộ 1A, Thanh Trì, Hà Nội', '02438990022', 'order@thudobeverage.vn', 'Nhà phân phối bia Heineken, Tiger, nước ngọt, khoáng');

INSERT INTO `tbl_nguyenlieu` (`id`, `manguyenlieu`, `tennguyenlieu`, `phanloai`, `soluongton`, `donvitinh`, `dongia`, `hansudung`) VALUES
(1, 'NL01', 'Thịt thăn bò tươi Úc', 'Thịt tươi sống', 120.5, 'kg', 240000, '2026-12-05'),
(2, 'NL02', 'Thịt ba chỉ bò Mỹ', 'Thịt tươi sống', 95.0, 'kg', 190000, '2026-12-08'),
(3, 'NL03', 'Thịt heo sinh học Ba Vì', 'Thịt tươi sống', 150.0, 'kg', 110000, '2026-12-01'),
(4, 'NL04', 'Xà lách Romaine hữu cơ', 'Rau củ', 45.0, 'kg', 35000, '2026-11-28'),
(5, 'NL05', 'Cà chua bi baby Đà Lạt', 'Rau củ', 60.0, 'kg', 40000, '2026-11-30'),
(6, 'NL06', 'Nấm đùi gà', 'Rau củ', 80.0, 'kg', 55000, '2026-12-02'),
(7, 'NL07', 'Tôm sú sống tự nhiên', 'Thủy hải sản', 70.0, 'kg', 280000, '2026-11-26'),
(8, 'NL08', 'Cá hồi Nauy tươi', 'Thủy hải sản', 40.0, 'kg', 320000, '2026-11-25'),
(9, 'NL09', 'Mực ống tươi loại 1', 'Thủy hải sản', 65.0, 'kg', 210000, '2026-11-29'),
(10, 'NL10', 'Gạo thơm ST25', 'Nông sản', 500.0, 'kg', 32000, '2027-05-15'),
(11, 'NL11', 'Dầu thực vật Simply', 'Gia vị đồ khô', 120.0, 'lít', 48000, '2027-08-20'),
(12, 'NL12', 'Nước mắm cá cơm', 'Gia vị đồ khô', 85.0, 'lít', 65000, '2027-10-10'),
(13, 'NL13', 'Bia Heineken lon 330ml', 'Đồ uống', 150.0, 'thùng', 410000, '2027-06-30');

INSERT INTO `tbl_hoadonnhap` (`id`, `mahoadonnhap`, `ngaynhap`, `id_nhacungcap`, `id_nhanvienkho`, `tongtien`, `ghichu`) VALUES
(1, 'HDN-20261005-01', '2026-10-05', 1, 3, 42500000, 'Nhập thịt bò Úc và thịt heo tươi định kỳ đầu tháng'),
(2, 'HDN-20261012-02', '2026-10-12', 2, 3, 8950000, 'Nhập rau xà lách, nấm tươi và cà chua'),
(3, 'HDN-20261018-03', '2026-10-18', 3, 3, 35600000, 'Nhập hải sản tươi sống tôm sú, cá hồi và mực'),
(4, 'HDN-20261025-04', '2026-10-25', 1, 3, 38200000, 'Nhập bổ sung thịt bò và ba chỉ'),
(5, 'HDN-20261102-05', '2026-11-02', 4, 3, 21500000, 'Nhập gạo ST25, dầu ăn và gia vị'),
(6, 'HDN-20261108-06', '2026-11-08', 2, 3, 11400000, 'Nhập rau củ sạch Đà Lạt đợt 1 tháng 11'),
(7, 'HDN-20261112-07', '2026-11-12', 3, 3, 42000000, 'Nhập tôm sú và cá hồi phục vụ sự kiện'),
(8, 'HDN-20261115-08', '2026-11-15', 5, 3, 32800000, 'Nhập bia Heineken và nước giải khát dự trữ'),
(9, 'HDN-20261118-09', '2026-11-18', 1, 3, 49000000, 'Nhập lô thịt bò cao cấp và heo sinh học'),
(10, 'HDN-20261120-10', '2026-11-20', 2, 3, 9800000, 'Nhập bổ sung rau quả tươi Đà Lạt');

INSERT INTO `tbl_hoadonnhapchitiet` (`id`, `id_hoadonnhap`, `id_nguyenlieu`, `soluong`, `dongianhap`, `thanhtien`) VALUES
(1, 1, 1, 120, 230000, 27600000),
(2, 1, 2, 60, 180000, 10800000),
(3, 1, 3, 41, 100000, 4100000),
(4, 2, 4, 100, 32000, 3200000),
(5, 2, 5, 80, 35000, 2800000),
(6, 2, 6, 55, 50000, 2750000),
(7, 3, 7, 60, 260000, 15600000),
(8, 3, 8, 40, 300000, 12000000),
(9, 3, 9, 40, 200000, 8000000),
(10, 4, 1, 100, 232000, 23200000),
(11, 4, 3, 150, 100000, 15000000),
(12, 5, 10, 300, 30000, 9000000),
(13, 5, 11, 150, 45000, 6750000),
(14, 5, 12, 95, 60000, 5700000),
(15, 6, 4, 150, 32000, 4800000),
(16, 6, 6, 80, 50000, 4000000),
(17, 6, 5, 70, 37000, 2590000),
(18, 7, 7, 80, 265000, 21200000),
(19, 7, 8, 55, 310000, 17050000),
(20, 8, 13, 80, 410000, 32800000),
(21, 9, 1, 150, 230000, 34500000),
(22, 9, 2, 80, 181250, 14500000),
(23, 10, 4, 120, 33000, 3960000),
(24, 10, 6, 60, 51000, 3060000),
(25, 10, 5, 75, 37000, 2775000);
