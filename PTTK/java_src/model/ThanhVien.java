package model;

import java.io.Serializable;
import java.util.Date;

public class ThanhVien implements Serializable {
    private int id;
    private String ten;
    private String tenDangNhap;
    private String matKhau;
    private Date ngaySinh;
    private String diaChi;
    private String email;
    private String soDienThoai;
    private String vaiTro;

    public ThanhVien() {}

    public ThanhVien(int id, String ten, String tenDangNhap, String matKhau, Date ngaySinh, String diaChi, String email, String soDienThoai, String vaiTro) {
        this.id = id;
        this.ten = ten;
        this.tenDangNhap = tenDangNhap;
        this.matKhau = matKhau;
        this.ngaySinh = ngaySinh;
        this.diaChi = diaChi;
        this.email = email;
        this.soDienThoai = soDienThoai;
        this.vaiTro = vaiTro;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getTen() { return ten; }
    public void setTen(String ten) { this.ten = ten; }
    public String getTenDangNhap() { return tenDangNhap; }
    public void setTenDangNhap(String tenDangNhap) { this.tenDangNhap = tenDangNhap; }
    public String getMatKhau() { return matKhau; }
    public void setMatKhau(String matKhau) { this.matKhau = matKhau; }
    public Date getNgaySinh() { return ngaySinh; }
    public void setNgaySinh(Date ngaySinh) { this.ngaySinh = ngaySinh; }
    public String getDiaChi() { return diaChi; }
    public void setDiaChi(String diaChi) { this.diaChi = diaChi; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getSoDienThoai() { return soDienThoai; }
    public void setSoDienThoai(String soDienThoai) { this.soDienThoai = soDienThoai; }
    public String getVaiTro() { return vaiTro; }
    public void setVaiTro(String vaiTro) { this.vaiTro = vaiTro; }
}
