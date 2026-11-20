package model;

import java.io.Serializable;

public class NhaCungCap implements Serializable {
    private int id;
    private String maNhaCungCap;
    private String ten;
    private String diaChi;
    private String soDienThoai;
    private String email;
    private String moTa;

    public NhaCungCap() {}

    public NhaCungCap(int id, String maNhaCungCap, String ten, String diaChi, String soDienThoai, String email, String moTa) {
        this.id = id;
        this.maNhaCungCap = maNhaCungCap;
        this.ten = ten;
        this.diaChi = diaChi;
        this.soDienThoai = soDienThoai;
        this.email = email;
        this.moTa = moTa;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getMaNhaCungCap() { return maNhaCungCap; }
    public void setMaNhaCungCap(String maNhaCungCap) { this.maNhaCungCap = maNhaCungCap; }
    public String getTen() { return ten; }
    public void setTen(String ten) { this.ten = ten; }
    public String getDiaChi() { return diaChi; }
    public void setDiaChi(String diaChi) { this.diaChi = diaChi; }
    public String getSoDienThoai() { return soDienThoai; }
    public void setSoDienThoai(String soDienThoai) { this.soDienThoai = soDienThoai; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getMoTa() { return moTa; }
    public void setMoTa(String moTa) { this.moTa = moTa; }
}
