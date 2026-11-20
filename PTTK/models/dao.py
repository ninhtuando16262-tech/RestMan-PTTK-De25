# ====================================================================
# LỚP TRUY XUẤT CƠ SỞ DỮ LIỆU (DAO - DATA ACCESS OBJECT)
# Thực hiện các phương thức xử lý nghiệp vụ theo đặc tả PTTK
# ====================================================================

import sqlite3
import os
from models.entities import (
    Thanhvien, Nhanvien, Nhanvienquanly, Nhanvienkho, Nhanvienbanhang, Khachhang,
    Monan, Nguyenlieu, Nhacungcap, Hoadonnhap, Hoadonnhapchitiet, TKnhacungcap
)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'restman.db')

class DAO:
    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

class MonAnDAO(DAO):
    """
    DAO xử lý dữ liệu món ăn theo biểu đồ lớp phân tích module Tìm kiếm món ăn
    Phương thức chính: timKiemMonan(), getChitietMonan()
    """
    def timKiemMonan(self, tukhoa=None):
        """
        Tìm kiếm danh sách món ăn theo từ khóa
        Ngoại lệ 3: Nếu khách hàng chưa nhập từ khóa hoặc từ khóa rỗng, hiển thị toàn bộ món ăn
        Ngoại lệ 4: Nếu không tìm thấy món ăn nào thì trả về danh sách rỗng
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if not tukhoa or not tukhoa.strip():
            query = "SELECT * FROM tbl_monan ORDER BY id ASC"
            cursor.execute(query)
        else:
            keyword = f"%{tukhoa.strip()}%"
            query = "SELECT * FROM tbl_monan WHERE tenmon LIKE ? OR loai LIKE ? OR mota LIKE ? ORDER BY id ASC"
            cursor.execute(query, (keyword, keyword, keyword))
            
        rows = cursor.fetchall()
        result = []
        for r in rows:
            monan = Monan(
                id=r['id'],
                mamon=r['mamon'],
                tenmon=r['tenmon'],
                loai=r['loai'],
                khauphan=r['khauphan'],
                giatien=r['giatien'],
                mota=r['mota'],
                hinhanh=r['hinhanh'],
                trangthai=r['trangthai']
            )
            result.append(monan)
            
        conn.close()
        return result

    def getChitietMonan(self, monan_id):
        """
        Lấy thông tin chi tiết một món ăn theo mã định danh (id)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM tbl_monan WHERE id = ?"
        cursor.execute(query, (monan_id,))
        r = cursor.fetchone()
        conn.close()
        
        if r:
            return Monan(
                id=r['id'],
                mamon=r['mamon'],
                tenmon=r['tenmon'],
                loai=r['loai'],
                khauphan=r['khauphan'],
                giatien=r['giatien'],
                mota=r['mota'],
                hinhanh=r['hinhanh'],
                trangthai=r['trangthai']
            )
        return None

class TKnhacungcapDAO(DAO):
    """
    DAO xử lý dữ liệu thống kê nhà cung cấp theo lượng hàng nhập
    Phương thức chính: getTKNhaCungCap(ngaybatdau, ngayketthuc)
    """
    def getTKNhaCungCap(self, ngaybatdau, ngayketthuc):
        """
        Thống kê các nhà cung cấp theo số lượng hàng nhập trong khoảng thời gian [ngaybatdau, ngayketthuc]
        Ngoại lệ: Nếu ngày bắt đầu > ngày kết thúc hoặc bỏ trống -> Báo lỗi
        """
        if not ngaybatdau or not ngayketthuc:
            raise ValueError("Khoảng thời gian thống kê không hợp lệ: Vui lòng nhập đầy đủ ngày bắt đầu và kết thúc.")
            
        if ngaybatdau > ngayketthuc:
            raise ValueError("Khoảng thời gian thống kê không hợp lệ: Ngày bắt đầu không thể lớn hơn ngày kết thúc.")
            
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                ncc.id,
                ncc.manhacungcap,
                ncc.ten,
                ncc.diachi,
                ncc.sdt,
                ncc.email,
                ncc.mota,
                COUNT(DISTINCT hd.id) as solannhap,
                COALESCE(SUM(ct.soluong), 0) as tongsoluongnhap,
                COALESCE(SUM(ct.thanhtien), 0) as tongtiennhap
            FROM tbl_nhacungcap ncc
            INNER JOIN tbl_hoadonnhap hd ON ncc.id = hd.id_nhacungcap
            INNER JOIN tbl_hoadonnhapchitiet ct ON hd.id = ct.id_hoadonnhap
            WHERE hd.ngaynhap >= ? AND hd.ngaynhap <= ?
            GROUP BY ncc.id
            ORDER BY tongsoluongnhap DESC, tongtiennhap DESC
        '''
        cursor.execute(query, (ngaybatdau, ngayketthuc))
        rows = cursor.fetchall()
        
        result = []
        for r in rows:
            tk_ncc = TKnhacungcap(
                id=r['id'],
                manhacungcap=r['manhacungcap'],
                ten=r['ten'],
                diachi=r['diachi'],
                sdt=r['sdt'],
                email=r['email'],
                mota=r['mota'],
                ngaybatdau=ngaybatdau,
                ngayketthuc=ngayketthuc,
                tongsoluongnhap=round(float(r['tongsoluongnhap']), 2),
                solannhap=int(r['solannhap']),
                tongtiennhap=float(r['tongtiennhap'])
            )
            result.append(tk_ncc)
            
        conn.close()
        return result

class HoaDonNhapDAO(DAO):
    """
    DAO xử lý danh sách các lần nhập nguyên liệu của nhà cung cấp
    Phương thức chính: getDSLanNhap(idNCC, ngaybatdau, ngayketthuc)
    """
    def getDSLanNhap(self, id_ncc, ngaybatdau=None, ngayketthuc=None):
        """
        Lấy danh sách các lần nhập nguyên liệu (hóa đơn nhập) của 1 nhà cung cấp trong khoảng thời gian
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Lấy thông tin nhà cung cấp
        cursor.execute("SELECT * FROM tbl_nhacungcap WHERE id = ?", (id_ncc,))
        ncc_row = cursor.fetchone()
        ncc = None
        if ncc_row:
            ncc = Nhacungcap(
                id=ncc_row['id'],
                manhacungcap=ncc_row['manhacungcap'],
                ten=ncc_row['ten'],
                diachi=ncc_row['diachi'],
                sdt=ncc_row['sdt'],
                email=ncc_row['email'],
                mota=ncc_row['mota']
            )
            
        params = [id_ncc]
        time_condition = ""
        if ngaybatdau and ngayketthuc:
            time_condition = "AND hd.ngaynhap >= ? AND hd.ngaynhap <= ?"
            params.extend([ngaybatdau, ngayketthuc])
            
        query = f'''
            SELECT 
                hd.*,
                nv.ten as ten_nhanvienkho,
                COALESCE(SUM(ct.soluong), 0) as tong_soluong_lan_nhap
            FROM tbl_hoadonnhap hd
            LEFT JOIN tbl_thanhvien nv ON hd.id_nhanvienkho = nv.id
            LEFT JOIN tbl_hoadonnhapchitiet ct ON hd.id = ct.id_hoadonnhap
            WHERE hd.id_nhacungcap = ? {time_condition}
            GROUP BY hd.id
            ORDER BY hd.ngaynhap DESC
        '''
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        
        result = []
        for r in rows:
            nvk = Nhanvienkho(id=r['id_nhanvienkho'], ten=r['ten_nhanvienkho'] or "Thủ kho")
            hd = Hoadonnhap(
                id=r['id'],
                mahoadonnhap=r['mahoadonnhap'],
                ngaynhap=r['ngaynhap'],
                id_nhacungcap=r['id_nhacungcap'],
                id_nhanvienkho=r['id_nhanvienkho'],
                tongtien=r['tongtien'],
                ghichu=r['ghichu'],
                nhacungcap=ncc,
                nhanvienkho=nvk
            )
            # Thêm trường phụ lưu tổng lượng nhập của hóa đơn đó
            hd.tong_soluong = round(float(r['tong_soluong_lan_nhap']), 2)
            result.append(hd)
            
        conn.close()
        return ncc, result

class HoaDonNhapChiTietDAO(DAO):
    """
    DAO xử lý thông tin chi tiết một hóa đơn nhập nguyên liệu
    Phương thức chính: getChiTietHoaDonNhap(idHDNhap)
    """
    def getChiTietHoaDonNhap(self, id_hd_nhap):
        """
        Lấy thông tin chi tiết của một hóa đơn nhập bao gồm danh sách các nguyên liệu nhập
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 1. Lấy thông tin hóa đơn chung
        query_hd = '''
            SELECT 
                hd.*,
                ncc.manhacungcap, ncc.ten as ten_ncc, ncc.diachi as diachi_ncc, ncc.sdt as sdt_ncc, ncc.email as email_ncc,
                nv.ten as ten_nhanvienkho
            FROM tbl_hoadonnhap hd
            INNER JOIN tbl_nhacungcap ncc ON hd.id_nhacungcap = ncc.id
            INNER JOIN tbl_thanhvien nv ON hd.id_nhanvienkho = nv.id
            WHERE hd.id = ?
        '''
        cursor.execute(query_hd, (id_hd_nhap,))
        hd_row = cursor.fetchone()
        if not hd_row:
            conn.close()
            return None
            
        ncc = Nhacungcap(
            id=hd_row['id_nhacungcap'],
            manhacungcap=hd_row['manhacungcap'],
            ten=hd_row['ten_ncc'],
            diachi=hd_row['diachi_ncc'],
            sdt=hd_row['sdt_ncc'],
            email=hd_row['email_ncc']
        )
        nvk = Nhanvienkho(
            id=hd_row['id_nhanvienkho'],
            ten=hd_row['ten_nhanvienkho']
        )
        
        hoadon = Hoadonnhap(
            id=hd_row['id'],
            mahoadonnhap=hd_row['mahoadonnhap'],
            ngaynhap=hd_row['ngaynhap'],
            id_nhacungcap=hd_row['id_nhacungcap'],
            id_nhanvienkho=hd_row['id_nhanvienkho'],
            tongtien=hd_row['tongtien'],
            ghichu=hd_row['ghichu'],
            nhacungcap=ncc,
            nhanvienkho=nvk
        )
        
        # 2. Lấy danh sách chi tiết nguyên liệu
        query_ct = '''
            SELECT 
                ct.*,
                nl.manguyenlieu, nl.tennguyenlieu, nl.phanloai, nl.donvitinh
            FROM tbl_hoadonnhapchitiet ct
            INNER JOIN tbl_nguyenlieu nl ON ct.id_nguyenlieu = nl.id
            WHERE ct.id_hoadonnhap = ?
            ORDER BY ct.id ASC
        '''
        cursor.execute(query_ct, (id_hd_nhap,))
        ct_rows = cursor.fetchall()
        
        danhsachchitiet = []
        for r in ct_rows:
            nl = Nguyenlieu(
                id=r['id_nguyenlieu'],
                manguyenlieu=r['manguyenlieu'],
                tennguyenlieu=r['tennguyenlieu'],
                phanloai=r['phanloai'],
                donvitinh=r['donvitinh']
            )
            item = Hoadonnhapchitiet(
                id=r['id'],
                id_hoadonnhap=r['id_hoadonnhap'],
                id_nguyenlieu=r['id_nguyenlieu'],
                soluong=float(r['soluong']),
                dongianhap=float(r['dongianhap']),
                thanhtien=float(r['thanhtien']),
                nguyenlieu=nl
            )
            danhsachchitiet.append(item)
            
        hoadon.danhsachchitiet = danhsachchitiet
        conn.close()
        return hoadon

class ThanhVienDAO(DAO):
    """
    DAO xử lý đăng nhập & xác thực người dùng
    """
    def kiemTraDangNhap(self, tendangnhap, matkhau):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM tbl_thanhvien WHERE tendangnhap = ? AND matkhau = ?"
        cursor.execute(query, (tendangnhap, matkhau))
        r = cursor.fetchone()
        conn.close()
        
        if not r:
            return None
            
        vaitro = r['vaitro']
        if vaitro == 'QuanLy':
            return Nhanvienquanly(id=r['id'], ten=r['ten'], tendangnhap=r['tendangnhap'], email=r['email'], sdt=r['sdt'], diachi=r['diachi'])
        elif vaitro == 'NhanVienKho':
            return Nhanvienkho(id=r['id'], ten=r['ten'], tendangnhap=r['tendangnhap'], email=r['email'], sdt=r['sdt'], diachi=r['diachi'])
        elif vaitro == 'NhanVienBanHang':
            return Nhanvienbanhang(id=r['id'], ten=r['ten'], tendangnhap=r['tendangnhap'], email=r['email'], sdt=r['sdt'], diachi=r['diachi'])
        else:
            return Khachhang(id=r['id'], ten=r['ten'], tendangnhap=r['tendangnhap'], email=r['email'], sdt=r['sdt'], diachi=r['diachi'])
