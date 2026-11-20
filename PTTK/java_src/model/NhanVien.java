package model;

public class NhanVien extends ThanhVien {
    private String viTriCongViec;

    public NhanVien() { super(); }

    public NhanVien(int id, String ten, String tenDangNhap, String matKhau, java.util.Date ngaySinh, String diaChi, String email, String soDienThoai, String vaiTro, String viTriCongViec) {
        super(id, ten, tenDangNhap, matKhau, ngaySinh, diaChi, email, soDienThoai, vaiTro);
        this.viTriCongViec = viTriCongViec;
    }

    public String getViTriCongViec() { return viTriCongViec; }
    public void setViTriCongViec(String viTriCongViec) { this.viTriCongViec = viTriCongViec; }
}
