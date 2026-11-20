package dao;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import model.HoaDonNhap;
import model.NhaCungCap;
import model.NhanVienKho;

public class HoaDonNhapDAO extends DAO {

    public HoaDonNhapDAO() {
        super();
    }

    /**
     * Lấy danh sách các lần nhập nguyên liệu của một nhà cung cấp theo khoảng thời gian
     */
    public List<HoaDonNhap> getDSLanNhap(int idNCC, Date ngayBatDau, Date ngayKetThuc) {
        List<HoaDonNhap> result = new ArrayList<>();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");

        String sql = "SELECT hd.*, nv.ten as ten_nhanvienkho, ncc.manhacungcap, ncc.ten as ten_ncc " +
                     "FROM tbl_hoadonnhap hd " +
                     "INNER JOIN tbl_nhacungcap ncc ON hd.id_nhacungcap = ncc.id " +
                     "LEFT JOIN tbl_thanhvien nv ON hd.id_nhanvienkho = nv.id " +
                     "WHERE hd.id_nhacungcap = ? ";

        if (ngayBatDau != null && ngayKetThuc != null) {
            sql += "AND hd.ngaynhap >= ? AND hd.ngaynhap <= ? ";
        }
        sql += "ORDER BY hd.ngaynhap DESC";

        try {
            PreparedStatement ps = con.prepareStatement(sql);
            ps.setInt(1, idNCC);
            if (ngayBatDau != null && ngayKetThuc != null) {
                ps.setString(2, sdf.format(ngayBatDau));
                ps.setString(3, sdf.format(ngayKetThuc));
            }
            ResultSet rs = ps.executeQuery();

            while (rs.next()) {
                HoaDonNhap hd = new HoaDonNhap();
                hd.setId(rs.getInt("id"));
                hd.setMaHoaDonNhap(rs.getString("mahoadonnhap"));
                hd.setTongTien(rs.getFloat("tongtien"));
                hd.setGhiChu(rs.getString("ghichu"));
                
                NhaCungCap ncc = new NhaCungCap();
                ncc.setId(idNCC);
                ncc.setMaNhaCungCap(rs.getString("manhacungcap"));
                ncc.setTen(rs.getString("ten_ncc"));
                hd.setNhaCungCap(ncc);

                NhanVienKho nvk = new NhanVienKho();
                nvk.setId(rs.getInt("id_nhanvienkho"));
                nvk.setTen(rs.getString("ten_nhanvienkho"));
                hd.setNhanVienKho(nvk);

                result.add(hd);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }
}
