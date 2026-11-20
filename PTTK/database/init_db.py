import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'restman.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    
    # 1. Seed Thành viên & Phân quyền
    users = [
        # (id, ten, tendangnhap, matkhau, ngaysinh, diachi, email, sdt, vaitro)
        (1, 'Nguyễn Văn An', 'khachhang1', '123456', '1998-05-15', '128 Cầu Giấy, Hà Nội', 'an.nv@gmail.com', '0912345678', 'KhachHang'),
        (2, 'Trần Thị Mai', 'quanly1', '123456', '1988-10-20', '45 Hoàng Hoa Thám, Ba Đình, Hà Nội', 'mai.tt@restman.vn', '0987654321', 'QuanLy'),
        (3, 'Lê Hoàng Nam', 'nhanvienkho1', '123456', '1995-03-12', '88 Trần Phú, Hà Đông, Hà Nội', 'nam.lh@restman.vn', '0933445566', 'NhanVienKho'),
        (4, 'Phạm Thu Hà', 'nhanvienbanhang1', '123456', '2001-08-25', '15 Chùa Bộc, Đống Đa, Hà Nội', 'ha.pt@restman.vn', '0977889900', 'NhanVienBanHang')
    ]
    cursor.executemany('''
        INSERT INTO tbl_thanhvien (id, ten, tendangnhap, matkhau, ngaysinh, diachi, email, sdt, vaitro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', users)
    
    # Thêm chi tiết nhân viên & khách hàng
    cursor.execute("INSERT INTO tbl_nhanvien (id, vitricongviec) VALUES (2, 'Quản lý vận hành')")
    cursor.execute("INSERT INTO tbl_nhanvien (id, vitricongviec) VALUES (3, 'Thủ kho thực phẩm')")
    cursor.execute("INSERT INTO tbl_nhanvien (id, vitricongviec) VALUES (4, 'Nhân viên phục vụ/bán hàng')")
    
    cursor.execute("INSERT INTO tbl_khachhang (id) VALUES (1)")
    cursor.execute("INSERT INTO tbl_the (mathe, id_khachhang, hangthe, ngaytao, diemtichluy) VALUES ('THE-VIP-001', 1, 'Vàng', '2026-01-10', 350)")
    
    # 2. Seed Món ăn (MonAn)
    dishes = [
        ('MA01', 'Phở bò tái gầu đặc biệt', 'Món chính', '1 người', 65000, 
         'Bò tái tươi ngon kết hợp cùng gầu giòn thơm ngon hảo hạng trong nước hầm xương đậm đà 24 giờ.',
         'https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=500', 'Đang phục vụ'),
        ('MA02', 'Bún chả Hà Nội truyền thống', 'Món chính', '1 người', 55000,
         'Chả miếng và chả băm nướng than hoa thơm lừng ăn kèm nem rán giòn tan, bún tươi và nước chấm chua ngọt.',
         'https://images.unsplash.com/photo-1544025162-d76694265947?w=500', 'Đang phục vụ'),
        ('MA03', 'Bò bít tết sốt tiêu đen', 'Món chính', '1-2 người', 135000,
         'Thịt thăn bò tươi nhập khẩu nướng mềm mọng, đậm đà với nước sốt tiêu đen cay nhẹ đặc trưng, dùng kèm bánh mì giòn.',
         'https://images.unsplash.com/photo-1558030006-450675393462?w=500', 'Đang phục vụ'),
        ('MA04', 'Lẩu hải sản chua cay thập cẩm', 'Món lẩu', '3-4 người', 380000,
         'Nước lẩu Tomyum đậm đà cay nồng hòa quyện tôm sú tươi, mực lá, nghêu, cá hồi và rau nấm tươi mát.',
         'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500', 'Đang phục vụ'),
        ('MA05', 'Nem hải sản chiên xù sốt Mayonnaise', 'Khai vị', '2-4 người', 75000,
         'Vỏ nem giòn rụm bọc nhân tôm mực ngọt thịt kết hợp sốt chấm thơm béo hấp dẫn.',
         'https://images.unsplash.com/photo-1541544741938-0af808871cc0?w=500', 'Đang phục vụ'),
        ('MA06', 'Cá hồi áp chảo sốt chanh leo', 'Món chính', '1 người', 185000,
         'Cá hồi Nauy áp chảo da giòn thịt ngọt mềm, phủ sốt chanh leo chua thanh và măng tây xào bơ tỏi.',
         'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=500', 'Đang phục vụ'),
        ('MA07', 'Gà nướng mật ong thảo mộc Tây Bắc', 'Món nướng', '2-3 người', 220000,
         'Gà ri thả vườn tẩm ướp hạt dổi mắc khén nướng than hồng da giòn óng ả màu mật ong rừng.',
         'https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=500', 'Đang phục vụ'),
        ('MA08', 'Salad cá ngừ rau củ hữu cơ', 'Khai vị', '1-2 người', 68000,
         'Cá ngừ đại dương áp chảo xé sợi trộn cùng xà lách Romaine, cà chua bi, trứng luộc và sốt mè rang.',
         'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=500', 'Đang phục vụ'),
        ('MA09', 'Mực một nắng nướng muối ớt xanh', 'Món nướng', '2-3 người', 160000,
         'Mực một nắng Phú Quốc dày mình nướng giòn ngọt, chấm muối ớt xanh cay tê nồng.',
         'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=500', 'Đang phục vụ'),
        ('MA10', 'Cơm chiên hải sản hoàng bào', 'Món chính', '1-2 người', 85000,
         'Hạt cơm dẻo thơm rang vàng óng bọc trứng mềm mịn kết hợp tôm, mực giòn ngọt và ngô ngọt.',
         'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=500', 'Đang phục vụ'),
        ('MA11', 'Trà đào cam sả hạt chia', 'Đồ uống', '1 người', 38000,
         'Trà đào hương thảo mộc thanh mát quyện cùng cam tươi mọng nước, sả thơm và hạt chia bổ dưỡng.',
         'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500', 'Đang phục vụ'),
        ('MA12', 'Chè sen long nhãn hạt sen Huế', 'Tráng miệng', '1 người', 32000,
         'Hạt sen bùi béo lồng khéo léo trong cùi nhãn ngọt giòn, nước đường phèn hoa bưởi thanh khiết.',
         'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=500', 'Đang phục vụ'),
        ('MA13', 'Súp hải sản bắp non trứng cút', 'Khai vị', '1 người', 45000,
         'Món súp sánh mịn thơm lừng với nhân tôm, mực tươi, cua xé sợi và bắp non ngọt thanh.',
         'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500', 'Đang phục vụ'),
        ('MA14', 'Nước ép dưa hấu bạc hà', 'Đồ uống', '1 người', 35000,
         'Dưa hấu nguyên chất ép lạnh tươi mát giải nhiệt tức thì kết hợp lá bạc hà the mát.',
         'https://images.unsplash.com/photo-1589733955941-5eeaf752f6dd?w=500', 'Đang phục vụ'),
        ('MA15', 'Kem dừa non cốt dừa Mã Lai', 'Tráng miệng', '1 người', 45000,
         'Kem dừa thơm béo mịn màng đặt trong trái dừa xiêm, rắc dừa sấy giòn tan và đậu phộng rang.',
         'https://images.unsplash.com/photo-1505394033641-40c6ad1178d7?w=500', 'Tạm ngưng')
    ]
    cursor.executemany('''
        INSERT INTO tbl_monan (mamon, tenmon, loai, khauphan, giatien, mota, hinhanh, trangthai)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', dishes)
    
    # 3. Seed Nhà cung cấp (NhaCungCap)
    suppliers = [
        ('NCC01', 'Công ty TNHH Thực phẩm Sạch Ba Vì', 'Xã Vân Hòa, Ba Vì, Hà Nội', '02433889911', 'bavifarm@cleanfood.vn', 'Cung cấp thịt bò tươi, thịt heo đạt chuẩn VietGAP và sữa sạch nguyên chất'),
        ('NCC02', 'Nông trại Rau Hữu cơ Đà Lạt EcoFarm', 'Phường 7, TP. Đà Lạt, Lâm Đồng', '02633778899', 'contact@dalatecofarm.vn', 'Chuyên cung cấp rau củ quả tươi, xà lách búp, nấm sạch và hoa quả nhiệt đới'),
        ('NCC03', 'Hải sản Tươi sống Biển Đông', 'Số 98 Cảng Cát Lái, Hải Phòng', '02253667788', 'kinhdoanh@biendongseafood.com', 'Cung cấp hải sản tôm sú tươi sống, cá hồi Nauy, mực một nắng và cua ghẹ'),
        ('NCC04', 'Tổng kho Nông sản & Gia vị Việt Hà', 'Lô B3 KCN Tiên Sơn, Bắc Ninh', '02223556677', 'vietha.spices@gmail.com', 'Phân phối gia vị đóng hộp, nước mắm truyền thống, gạo ngon ST25 và dầu ăn thực vật'),
        ('NCC05', 'Công ty Đồ uống & Nước giải khát Thủ Đô', 'Km 10 Quốc lộ 1A, Thanh Trì, Hà Nội', '02438990022', 'order@thudobeverage.vn', 'Nhà phân phối bia Heineken, Tiger, nước ngọt Coca-Cola, trà và khoáng Lavie')
    ]
    cursor.executemany('''
        INSERT INTO tbl_nhacungcap (manhacungcap, ten, diachi, sdt, email, mota)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', suppliers)
    
    # 4. Seed Nguyên liệu (NguyenLieu)
    materials = [
        # (manguyenlieu, tennguyenlieu, phanloai, soluongton, donvitinh, dongia, hansudung)
        ('NL01', 'Thịt thăn bò tươi Úc', 'Thịt tươi sống', 120.5, 'kg', 240000, '2026-12-05'),
        ('NL02', 'Thịt ba chỉ bò Mỹ', 'Thịt tươi sống', 95.0, 'kg', 190000, '2026-12-08'),
        ('NL03', 'Thịt heo sinh học Ba Vì', 'Thịt tươi sống', 150.0, 'kg', 110000, '2026-12-01'),
        ('NL04', 'Xà lách Romaine hữu cơ', 'Rau củ', 45.0, 'kg', 35000, '2026-11-28'),
        ('NL05', 'Cà chua bi baby Đà Lạt', 'Rau củ', 60.0, 'kg', 40000, '2026-11-30'),
        ('NL06', 'Nấm kim châm & Nấm đùi gà', 'Rau củ', 80.0, 'kg', 55000, '2026-12-02'),
        ('NL07', 'Tôm sú sống tự nhiên', 'Thủy hải sản', 70.0, 'kg', 280000, '2026-11-26'),
        ('NL08', 'Cá hồi Nauy tươi nguyên con', 'Thủy hải sản', 40.0, 'kg', 320000, '2026-11-25'),
        ('NL09', 'Mực ống tươi loại 1', 'Thủy hải sản', 65.0, 'kg', 210000, '2026-11-29'),
        ('NL10', 'Gạo thơm ST25 Thượng hạng', 'Nông sản', 500.0, 'kg', 32000, '2027-05-15'),
        ('NL11', 'Dầu thực vật cao cấp Simply', 'Gia vị đồ khô', 120.0, 'lít', 48000, '2027-08-20'),
        ('NL12', 'Nước mắm cá cơm Phan Thiết 40 độ', 'Gia vị đồ khô', 85.0, 'lít', 65000, '2027-10-10'),
        ('NL13', 'Bia Heineken lon 330ml', 'Đồ uống', 150.0, 'thùng', 410000, '2027-06-30'),
        ('NL14', 'Trà đen Ceylon hảo hạng', 'Đồ khô', 25.0, 'kg', 120000, '2027-12-31')
    ]
    cursor.executemany('''
        INSERT INTO tbl_nguyenlieu (manguyenlieu, tennguyenlieu, phanloai, soluongton, donvitinh, dongia, hansudung)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', materials)
    
    # 5. Seed Hóa đơn nhập & Chi tiết hóa đơn nhập (Phục vụ Module Thống kê NCC)
    # Chúng ta lập danh sách hóa đơn trải từ tháng 10/2026 đến tháng 11/2026
    invoices = [
        # (id, mahoadonnhap, ngaynhap, id_nhacungcap, id_nhanvienkho, tongtien, ghichu)
        (1, 'HDN-20261005-01', '2026-10-05', 1, 3, 42500000, 'Nhập thịt bò Úc và thịt heo tươi định kỳ đầu tháng'),
        (2, 'HDN-20261012-02', '2026-10-12', 2, 3, 8950000, 'Nhập rau xà lách, nấm tươi và cà chua phục vụ cuối tuần'),
        (3, 'HDN-20261018-03', '2026-10-18', 3, 3, 35600000, 'Nhập hải sản tươi sống tôm sú, cá hồi và mực'),
        (4, 'HDN-20261025-04', '2026-10-25', 1, 3, 38200000, 'Nhập bổ sung thịt bò và ba chỉ chuẩn bị tiệc hội nghị'),
        (5, 'HDN-20261102-05', '2026-11-02', 4, 3, 21500000, 'Nhập gạo ST25, dầu ăn Simply và gia vị các loại'),
        (6, 'HDN-20261108-06', '2026-11-08', 2, 3, 11400000, 'Nhập rau củ sạch Đà Lạt đợt 1 tháng 11'),
        (7, 'HDN-20261112-07', '2026-11-12', 3, 3, 42000000, 'Nhập tôm sú và cá hồi phục vụ sự kiện khách sạn'),
        (8, 'HDN-20261115-08', '2026-11-15', 5, 3, 32800000, 'Nhập bia Heineken và nước giải khát dự trữ'),
        (9, 'HDN-20261118-09', '2026-11-18', 1, 3, 49000000, 'Nhập lô thịt bò cao cấp và heo sinh học chuẩn bị lễ hội ẩm thực'),
        (10, 'HDN-20261120-10', '2026-11-20', 2, 3, 9800000, 'Nhập bổ sung rau quả tươi Đà Lạt giao trong ngày')
    ]
    cursor.executemany('''
        INSERT INTO tbl_hoadonnhap (id, mahoadonnhap, ngaynhap, id_nhacungcap, id_nhanvienkho, tongtien, ghichu)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', invoices)
    
    # Chi tiết hóa đơn nhập
    invoice_details = [
        # (id_hoadonnhap, id_nguyenlieu, soluong, dongianhap, thanhtien)
        # HDN 1: NCC 1 (Thịt bò 120kg, Heo 130kg) -> Tổng = 120*230000 + 130*100000 = 27.6M + 13M = 40.6M
        (1, 1, 120, 230000, 27600000),
        (1, 2, 60, 180000, 10800000),
        (1, 3, 41, 100000, 4100000), # Tổng = 42.5M
        
        # HDN 2: NCC 2 (Rau củ: Xà lách 100kg, Cà chua 80kg, Nấm 55kg)
        (2, 4, 100, 32000, 3200000),
        (2, 5, 80, 35000, 2800000),
        (2, 6, 55, 50000, 2750000),
        (2, 4, 6.25, 32000, 200000), # Tổng = 8.95M
        
        # HDN 3: NCC 3 (Tôm sú 60kg, Cá hồi 40kg, Mực 50kg)
        (3, 7, 60, 260000, 15600000),
        (3, 8, 40, 300000, 12000000),
        (3, 9, 40, 200000, 8000000), # Tổng = 35.6M
        
        # HDN 4: NCC 1 (Thịt bò 100kg, Heo 150kg)
        (4, 1, 100, 232000, 23200000),
        (4, 3, 150, 100000, 15000000), # Tổng = 38.2M
        
        # HDN 5: NCC 4 (Gạo 300kg, Dầu 150L, Nước mắm 80L)
        (5, 10, 300, 30000, 9000000),
        (5, 11, 150, 45000, 6750000),
        (5, 12, 95, 60000, 5700000), # Tổng = 21.45M ~ 21.5M
        
        # HDN 6: NCC 2 (Xà lách 150kg, Nấm 80kg, Cà chua 70kg)
        (6, 4, 150, 32000, 4800000),
        (6, 6, 80, 50000, 4000000),
        (6, 5, 70, 37000, 2590000),
        (6, 4, 0.31, 32000, 10000), # Tổng = 11.4M
        
        # HDN 7: NCC 3 (Tôm sú 80kg, Cá hồi 55kg, Mực 30kg)
        (7, 7, 80, 265000, 21200000),
        (7, 8, 50, 310000, 15500000),
        (7, 9, 25, 212000, 5300000), # Tổng = 42M
        
        # HDN 8: NCC 5 (Bia 80 thùng)
        (8, 13, 80, 410000, 32800000), # Tổng = 32.8M
        
        # HDN 9: NCC 1 (Thịt bò 150kg, Heo 140kg)
        (9, 1, 150, 230000, 34500000),
        (9, 2, 80, 181250, 14500000), # Tổng = 49M
        
        # HDN 10: NCC 2 (Xà lách 120kg, Nấm 60kg, Cà chua 80kg)
        (10, 4, 120, 33000, 3960000),
        (10, 6, 60, 51000, 3060000),
        (10, 5, 75, 37000, 2775000),
        (10, 4, 0.15, 33000, 5000) # Tổng = 9.8M
    ]
    cursor.executemany('''
        INSERT INTO tbl_hoadonnhapchitiet (id_hoadonnhap, id_nguyenlieu, soluong, dongianhap, thanhtien)
        VALUES (?, ?, ?, ?, ?)
    ''', invoice_details)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully at:", DB_PATH)

if __name__ == '__main__':
    init_database()
