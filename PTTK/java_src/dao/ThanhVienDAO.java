package dao;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import model.KhachHang;
import model.NhanVienBanHang;
import model.NhanVienKho;
import model.NhanVienQuanLy;
import model.ThanhVien;

public class ThanhVienDAO extends DAO {

    public ThanhVienDAO() {
        super();
    }

    /**
     * Xác thực đăng nhập hệ thống
     */
    public ThanhVien kiemTraDangNhap(String tenDangNhap, String matKhau) {
        ThanhVien tv = null;
        String sql = "SELECT * FROM tbl_thanhvien WHERE tendangnhap = ? AND matkhau = ?";
        try {
            PreparedStatement ps = con.prepareStatement(sql);
            ps.setString(1, tenDangNhap);
            ps.setString(2, matKhau);
            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                String vaiTro = rs.getString("vaitro");
                if ("QuanLy".equalsIgnoreCase(vaiTro)) {
                    tv = new NhanVienQuanLy();
                } else if ("NhanVienKho".equalsIgnoreCase(vaiTro)) {
                    tv = new NhanVienKho();
                } else if ("NhanVienBanHang".equalsIgnoreCase(vaiTro)) {
                    tv = new NhanVienBanHang();
                } else {
                    tv = new KhachHang();
                }
                tv.setId(rs.getInt("id"));
                tv.setTen(rs.getString("ten"));
                tv.setTenDangNhap(rs.getString("tendangnhap"));
                tv.setEmail(rs.getString("email"));
                tv.setSoDienThoai(rs.getString("sdt"));
                tv.setDiaChi(rs.getString("diachi"));
                tv.setVaiTro(vaiTro);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return tv;
    }
}
