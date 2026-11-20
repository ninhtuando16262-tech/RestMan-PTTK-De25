package dao;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import model.TKnhacungcap;

public class TKnhacungcapDAO extends DAO {

    public TKnhacungcapDAO() {
        super();
    }

    /**
     * Thống kê nhà cung cấp theo số lượng hàng nhập trong khoảng thời gian [ngayBatDau, ngayKetThuc]
     * Sắp xếp theo tổng lượng nhập giảm dần
     */
    public List<TKnhacungcap> getTKNhaCungCap(Date ngayBatDau, Date ngayKetThuc) throws Exception {
        if (ngayBatDau == null || ngayKetThuc == null) {
            throw new IllegalArgumentException("Khoảng thời gian thống kê không hợp lệ: Vui lòng chọn đầy đủ ngày bắt đầu và ngày kết thúc.");
        }
        if (ngayBatDau.after(ngayKetThuc)) {
            throw new IllegalArgumentException("Khoảng thời gian thống kê không hợp lệ: Ngày bắt đầu không thể sau ngày kết thúc.");
        }

        List<TKnhacungcap> result = new ArrayList<>();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        String strBatDau = sdf.format(ngayBatDau);
        String strKetThuc = sdf.format(ngayKetThuc);

        String sql = "SELECT " +
                     "    ncc.id, ncc.manhacungcap, ncc.ten, ncc.diachi, ncc.sdt, ncc.email, ncc.mota, " +
                     "    COUNT(DISTINCT hd.id) as solannhap, " +
                     "    COALESCE(SUM(ct.soluong), 0) as tongsoluongnhap, " +
                     "    COALESCE(SUM(ct.thanhtien), 0) as tongtiennhap " +
                     "FROM tbl_nhacungcap ncc " +
                     "INNER JOIN tbl_hoadonnhap hd ON ncc.id = hd.id_nhacungcap " +
                     "INNER JOIN tbl_hoadonnhapchitiet ct ON hd.id = ct.id_hoadonnhap " +
                     "WHERE hd.ngaynhap >= ? AND hd.ngaynhap <= ? " +
                     "GROUP BY ncc.id " +
                     "ORDER BY tongsoluongnhap DESC, tongtiennhap DESC";

        try {
            PreparedStatement ps = con.prepareStatement(sql);
            ps.setString(1, strBatDau);
            ps.setString(2, strKetThuc);
            ResultSet rs = ps.executeQuery();

            while (rs.next()) {
                TKnhacungcap tk = new TKnhacungcap();
                tk.setId(rs.getInt("id"));
                tk.setMaNhaCungCap(rs.getString("manhacungcap"));
                tk.setTen(rs.getString("ten"));
                tk.setDiaChi(rs.getString("diachi"));
                tk.setSoDienThoai(rs.getString("sdt"));
                tk.setEmail(rs.getString("email"));
                tk.setMoTa(rs.getString("mota"));
                tk.setNgayBatDau(ngayBatDau);
                tk.setNgayKetThuc(ngayKetThuc);
                tk.setTongSoLuongNhap(rs.getFloat("tongsoluongnhap"));
                tk.setSoLanNhap(rs.getInt("solannhap"));
                tk.setTongTienNhap(rs.getFloat("tongtiennhap"));
                result.add(tk);
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw e;
        }
        return result;
    }
}
