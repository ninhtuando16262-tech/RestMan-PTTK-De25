# ====================================================================
# KIỂM THỬ ĐƠN VỊ (UNIT TEST) CHO CÁC LỚP DAO
# ====================================================================

import unittest
import sys
import os

# Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.dao import MonAnDAO, TKnhacungcapDAO, HoaDonNhapDAO, HoaDonNhapChiTietDAO, ThanhVienDAO

class TestRestManDAOs(unittest.TestCase):
    def setUp(self):
        self.monan_dao = MonAnDAO()
        self.tk_dao = TKnhacungcapDAO()
        self.hd_dao = HoaDonNhapDAO()
        self.hd_ct_dao = HoaDonNhapChiTietDAO()
        self.tv_dao = ThanhVienDAO()

    # --- TEST MODULE 1: TÌM KIẾM MÓN ĂN ---
    def test_timKiemMonan_all_when_empty_keyword(self):
        """Ngoại lệ 3: Nếu từ khóa rỗng, hiển thị toàn bộ món ăn"""
        dishes = self.monan_dao.timKiemMonan("")
        self.assertGreaterEqual(len(dishes), 10)

    def test_timKiemMonan_found(self):
        """Kịch bản chính: Tìm kiếm theo từ khóa có kết quả"""
        dishes = self.monan_dao.timKiemMonan("bò")
        self.assertGreater(len(dishes), 0)
        for d in dishes:
            self.assertTrue("bò" in d.tenmon.lower() or "bò" in d.mota.lower())

    def test_timKiemMonan_not_found(self):
        """Ngoại lệ 4: Không tìm thấy món ăn nào nếu từ khóa không khớp"""
        dishes = self.monan_dao.timKiemMonan("mon_khong_ton_tai_xyz123")
        self.assertEqual(len(dishes), 0)

    def test_getChitietMonan(self):
        """Xem chi tiết món ăn theo ID"""
        dish = self.monan_dao.getChitietMonan(1)
        self.assertIsNotNone(dish)
        self.assertEqual(dish.id, 1)
        self.assertTrue(len(dish.tenmon) > 0)
        self.assertTrue(dish.giatien > 0)

    # --- TEST MODULE 2: THỐNG KÊ NHÀ CUNG CẤP ---
    def test_getTKNhaCungCap_valid(self):
        """Kịch bản chính: Thống kê nhà cung cấp trong khoảng thời gian hợp lệ"""
        stats = self.tk_dao.getTKNhaCungCap("2026-10-01", "2026-11-21")
        self.assertGreater(len(stats), 0)
        # Kiểm tra sắp xếp theo tổng lượng nhập giảm dần
        for i in range(len(stats) - 1):
            self.assertGreaterEqual(stats[i].tongsoluongnhap, stats[i+1].tongsoluongnhap)

    def test_getTKNhaCungCap_invalid_date_range(self):
        """Ngoại lệ: Ngày bắt đầu > Ngày kết thúc phải ném ngoại lệ ValueError"""
        with self.assertRaises(ValueError):
            self.tk_dao.getTKNhaCungCap("2026-11-30", "2026-10-01")

    def test_getTKNhaCungCap_empty_date(self):
        """Ngoại lệ: Bỏ trống ngày bắt đầu hoặc kết thúc"""
        with self.assertRaises(ValueError):
            self.tk_dao.getTKNhaCungCap("", "2026-10-01")

    def test_getTKNhaCungCap_no_data(self):
        """Khoảng thời gian không có phát sinh nhập hàng"""
        stats = self.tk_dao.getTKNhaCungCap("2020-01-01", "2020-01-05")
        self.assertEqual(len(stats), 0)

    def test_getDSLanNhap(self):
        """Lấy danh sách các lần nhập của 1 NCC"""
        ncc, invoices = self.hd_dao.getDSLanNhap(1, "2026-10-01", "2026-11-21")
        self.assertIsNotNone(ncc)
        self.assertEqual(ncc.id, 1)
        self.assertGreater(len(invoices), 0)

    def test_getChiTietHoaDonNhap(self):
        """Lấy chi tiết 1 hóa đơn nhập"""
        invoice = self.hd_ct_dao.getChiTietHoaDonNhap(1)
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.id, 1)
        self.assertIsNotNone(invoice.nhacungcap)
        self.assertIsNotNone(invoice.nhanvienkho)
        self.assertGreater(len(invoice.danhsachchitiet), 0)

    # --- TEST AUTH ---
    def test_kiemTraDangNhap_success(self):
        user = self.tv_dao.kiemTraDangNhap("quanly1", "123456")
        self.assertIsNotNone(user)
        self.assertEqual(user.vaitro, "QuanLy")

    def test_kiemTraDangNhap_fail(self):
        user = self.tv_dao.kiemTraDangNhap("quanly1", "sai_mat_khau")
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
