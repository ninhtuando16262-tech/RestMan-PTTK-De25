# ====================================================================
# LỚP THỰC THỂ (ENTITIES) - HỆ THỐNG RESTMAN
# Tuân thủ theo Sơ đồ lớp thực thể & Phân tích thiết kế hệ thống
# ====================================================================

class Thanhvien:
    def __init__(self, id=None, ten="", tendangnhap="", matkhau="", ngaysinh="", diachi="", email="", sdt="", vaitro=""):
        self.id = id
        self.ten = ten
        self.tendangnhap = tendangnhap
        self.matkhau = matkhau
        self.ngaysinh = ngaysinh
        self.diachi = diachi
        self.email = email
        self.sdt = sdt
        self.vaitro = vaitro

class Nhanvien(Thanhvien):
    def __init__(self, id=None, ten="", tendangnhap="", matkhau="", ngaysinh="", diachi="", email="", sdt="", vaitro="NhanVien", vitricongviec=""):
        super().__init__(id, ten, tendangnhap, matkhau, ngaysinh, diachi, email, sdt, vaitro)
        self.vitricongviec = vitricongviec

class Nhanvienquanly(Nhanvien):
    def __init__(self, id=None, ten="", tendangnhap="", matkhau="", ngaysinh="", diachi="", email="", sdt="", vitricongviec="Quản lý"):
        super().__init__(id, ten, tendangnhap, matkhau, ngaysinh, diachi, email, sdt, "QuanLy", vitricongviec)

class Nhanvienkho(Nhanvien):
    def __init__(self, id=None, ten="", tendangnhap="", matkhau="", ngaysinh="", diachi="", email="", sdt="", vitricongviec="Thủ kho"):
        super().__init__(id, ten, tendangnhap, matkhau, ngaysinh, diachi, email, sdt, "NhanVienKho", vitricongviec)

class Nhanvienbanhang(Nhanvien):
    def __init__(self, id=None, ten="", tendangnhap="", matkhau="", ngaysinh="", diachi="", email="", sdt="", vitricongviec="Bán hàng"):
        super().__init__(id, ten, tendangnhap, matkhau, ngaysinh, diachi, email, sdt, "NhanVienBanHang", vitricongviec)

class Khachhang(Thanhvien):
    def __init__(self, id=None, ten="", tendangnhap="", matkhau="", ngaysinh="", diachi="", email="", sdt=""):
        super().__init__(id, ten, tendangnhap, matkhau, ngaysinh, diachi, email, sdt, "KhachHang")

class Monan:
    def __init__(self, id=None, mamon="", tenmon="", loai="", khauphan="", giatien=0.0, mota="", hinhanh="", trangthai="Đang phục vụ"):
        self.id = id
        self.mamon = mamon
        self.tenmon = tenmon
        self.loai = loai
        self.khauphan = khauphan
        self.giatien = giatien
        self.mota = mota
        self.hinhanh = hinhanh
        self.trangthai = trangthai

class Nguyenlieu:
    def __init__(self, id=None, manguyenlieu="", tennguyenlieu="", phanloai="", soluongton=0.0, donvitinh="", dongia=0.0, hansudung=""):
        self.id = id
        self.manguyenlieu = manguyenlieu
        self.tennguyenlieu = tennguyenlieu
        self.phanloai = phanloai
        self.soluongton = soluongton
        self.donvitinh = donvitinh
        self.dongia = dongia
        self.hansudung = hansudung

class Nhacungcap:
    def __init__(self, id=None, manhacungcap="", ten="", diachi="", sdt="", email="", mota=""):
        self.id = id
        self.manhacungcap = manhacungcap
        self.ten = ten
        self.diachi = diachi
        self.sdt = sdt
        self.email = email
        self.mota = mota

class Hoadonnhap:
    def __init__(self, id=None, mahoadonnhap="", ngaynhap="", id_nhacungcap=None, id_nhanvienkho=None, tongtien=0.0, ghichu="", nhacungcap=None, nhanvienkho=None, danhsachchitiet=None):
        self.id = id
        self.mahoadonnhap = mahoadonnhap
        self.ngaynhap = ngaynhap
        self.id_nhacungcap = id_nhacungcap
        self.id_nhanvienkho = id_nhanvienkho
        self.tongtien = tongtien
        self.ghichu = ghichu
        self.nhacungcap = nhacungcap
        self.nhanvienkho = nhanvienkho
        self.danhsachchitiet = danhsachchitiet or []

class Hoadonnhapchitiet:
    def __init__(self, id=None, id_hoadonnhap=None, id_nguyenlieu=None, soluong=0.0, dongianhap=0.0, thanhtien=0.0, nguyenlieu=None):
        self.id = id
        self.id_hoadonnhap = id_hoadonnhap
        self.id_nguyenlieu = id_nguyenlieu
        self.soluong = soluong
        self.dongianhap = dongianhap
        self.thanhtien = thanhtien
        self.nguyenlieu = nguyenlieu

class TKnhacungcap(Nhacungcap):
    """
    Lớp Thống kê nhà cung cấp, kế thừa Nhacungcap, bổ sung các thuộc tính phục vụ thống kê:
    ngaybatdau, ngayketthuc, tongsoluongnhap, solannhap, tongtiennhap
    """
    def __init__(self, id=None, manhacungcap="", ten="", diachi="", sdt="", email="", mota="", 
                 ngaybatdau="", ngayketthuc="", tongsoluongnhap=0.0, solannhap=0, tongtiennhap=0.0):
        super().__init__(id, manhacungcap, ten, diachi, sdt, email, mota)
        self.ngaybatdau = ngaybatdau
        self.ngayketthuc = ngayketthuc
        self.tongsoluongnhap = tongsoluongnhap
        self.solannhap = solannhap
        self.tongtiennhap = tongtiennhap
