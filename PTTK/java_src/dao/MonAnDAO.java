package dao;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;
import model.MonAn;

public class MonAnDAO extends DAO {

    public MonAnDAO() {
        super();
    }

    /**
     * Tìm kiếm món ăn theo từ khóa
     * Ngoại lệ 3: Nếu từ khóa rỗng, hiển thị toàn bộ danh sách món ăn
     * Ngoại lệ 4: Nếu không có món ăn phù hợp, trả về danh sách rỗng
     */
    public List<MonAn> timKiemMonan(String tuKhoa) {
        List<MonAn> result = new ArrayList<>();
        String sql;
        try {
            PreparedStatement ps;
            if (tuKhoa == null || tuKhoa.trim().isEmpty()) {
                sql = "SELECT * FROM tbl_monan ORDER BY id ASC";
                ps = con.prepareStatement(sql);
            } else {
                sql = "SELECT * FROM tbl_monan WHERE tenmon LIKE ? OR loai LIKE ? OR mota LIKE ? ORDER BY id ASC";
                ps = con.prepareStatement(sql);
                String keyword = "%" + tuKhoa.trim() + "%";
                ps.setString(1, keyword);
                ps.setString(2, keyword);
                ps.setString(3, keyword);
            }
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                MonAn mon = new MonAn();
                mon.setId(rs.getInt("id"));
                mon.setMaMon(rs.getString("mamon"));
                mon.setTenMon(rs.getString("tenmon"));
                mon.setLoai(rs.getString("loai"));
                mon.setKhauPhan(rs.getString("khauphan"));
                mon.setGiaTien(rs.getFloat("giatien"));
                mon.setMoTa(rs.getString("mota"));
                mon.setHinhAnh(rs.getString("hinhanh"));
                mon.setTrangThai(rs.getString("trangthai"));
                result.add(mon);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }

    /**
     * Lấy thông tin chi tiết món ăn theo mã định danh (id)
     */
    public MonAn getChitietMonan(int id) {
        MonAn mon = null;
        String sql = "SELECT * FROM tbl_monan WHERE id = ?";
        try {
            PreparedStatement ps = con.prepareStatement(sql);
            ps.setInt(1, id);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) {
                mon = new MonAn();
                mon.setId(rs.getInt("id"));
                mon.setMaMon(rs.getString("mamon"));
                mon.setTenMon(rs.getString("tenmon"));
                mon.setLoai(rs.getString("loai"));
                mon.setKhauPhan(rs.getString("khauphan"));
                mon.setGiaTien(rs.getFloat("giatien"));
                mon.setMoTa(rs.getString("mota"));
                mon.setHinhAnh(rs.getString("hinhanh"));
                mon.setTrangThai(rs.getString("trangthai"));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return mon;
    }
}
