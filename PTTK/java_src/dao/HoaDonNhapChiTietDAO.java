package dao;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;
import model.HoaDonNhap;
import model.HoaDonNhapChiTiet;
import model.NguyenLieu;
import model.NhaCungCap;
import model.NhanVienKho;

public class HoaDonNhapChiTietDAO extends DAO {

    public HoaDonNhapChiTietDAO() {
        super();
    }

    /**
     * Lấy thông tin chi tiết một hóa đơn nhập kèm danh sách các dòng nguyên liệu
     */
    public HoaDonNhap getChiTietHoaDonNhap(int idHDNhap) {
        HoaDonNhap hd = null;
        try {
            // 1. Lấy thông tin chung hóa đơn
            String sqlHD = "SELECT hd.*, ncc.manhacungcap, ncc.ten as ten_ncc, ncc.diachi as diachi_ncc, " +
                           "       ncc.sdt as sdt_ncc, ncc.email as email_ncc, nv.ten as ten_nhanvienkho " +
                           "FROM tbl_hoadonnhap hd " +
                           "INNER JOIN tbl_nhacungcap ncc ON hd.id_nhacungcap = ncc.id " +
                           "INNER JOIN tbl_thanhvien nv ON hd.id_nhanvienkho = nv.id " +
                           "WHERE hd.id = ?";
            PreparedStatement psHD = con.prepareStatement(sqlHD);
            psHD.setInt(1, idHDNhap);
            ResultSet rsHD = psHD.executeQuery();

            if (rsHD.next()) {
                hd = new HoaDonNhap();
                hd.setId(rsHD.getInt("id"));
                hd.setMaHoaDonNhap(rsHD.getString("mahoadonnhap"));
                hd.setTongTien(rsHD.getFloat("tongtien"));
                hd.setGhiChu(rsHD.getString("ghichu"));

                NhaCungCap ncc = new NhaCungCap();
                ncc.setId(rsHD.getInt("id_nhacungcap"));
                ncc.setMaNhaCungCap(rsHD.getString("manhacungcap"));
                ncc.setTen(rsHD.getString("ten_ncc"));
                ncc.setDiaChi(rsHD.getString("diachi_ncc"));
                ncc.setSoDienThoai(rsHD.getString("sdt_ncc"));
                ncc.setEmail(rsHD.getString("email_ncc"));
                hd.setNhaCungCap(ncc);

                NhanVienKho nvk = new NhanVienKho();
                nvk.setId(rsHD.getInt("id_nhanvienkho"));
                nvk.setTen(rsHD.getString("ten_nhanvienkho"));
                hd.setNhanVienKho(nvk);

                // 2. Lấy chi tiết các mặt hàng nguyên liệu
                String sqlCT = "SELECT ct.*, nl.manguyenlieu, nl.tennguyenlieu, nl.phanloai, nl.donvitinh " +
                               "FROM tbl_hoadonnhapchitiet ct " +
                               "INNER JOIN tbl_nguyenlieu nl ON ct.id_nguyenlieu = nl.id " +
                               "WHERE ct.id_hoadonnhap = ? ORDER BY ct.id ASC";
                PreparedStatement psCT = con.prepareStatement(sqlCT);
                psCT.setInt(1, idHDNhap);
                ResultSet rsCT = psCT.executeQuery();

                List<HoaDonNhapChiTiet> dsChiTiet = new ArrayList<>();
                while (rsCT.next()) {
                    HoaDonNhapChiTiet ct = new HoaDonNhapChiTiet();
                    ct.setId(rsCT.getInt("id"));
                    ct.setIdHoaDonNhap(idHDNhap);
                    ct.setSoLuong(rsCT.getFloat("soluong"));
                    ct.setDonGiaNhap(rsCT.getFloat("dongianhap"));
                    ct.setThanhTien(rsCT.getFloat("thanhtien"));

                    NguyenLieu nl = new NguyenLieu();
                    nl.setId(rsCT.getInt("id_nguyenlieu"));
                    nl.setMaNguyenLieu(rsCT.getString("manguyenlieu"));
                    nl.setTenNguyenLieu(rsCT.getString("tennguyenlieu"));
                    nl.setPhanLoai(rsCT.getString("phanloai"));
                    nl.setDonViTinh(rsCT.getString("donvitinh"));
                    ct.setNguyenLieu(nl);

                    dsChiTiet.add(ct);
                }
                hd.setDanhSachChiTiet(dsChiTiet);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return hd;
    }
}
