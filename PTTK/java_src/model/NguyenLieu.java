package model;

import java.io.Serializable;
import java.util.Date;

public class NguyenLieu implements Serializable {
    private int id;
    private String maNguyenLieu;
    private String tenNguyenLieu;
    private String phanLoai;
    private float soLuongTon;
    private String donViTinh;
    private float donGia;
    private Date hanSuDung;

    public NguyenLieu() {}

    public NguyenLieu(int id, String maNguyenLieu, String tenNguyenLieu, String phanLoai, float soLuongTon, String donViTinh, float donGia, Date hanSuDung) {
        this.id = id;
        this.maNguyenLieu = maNguyenLieu;
        this.tenNguyenLieu = tenNguyenLieu;
        this.phanLoai = phanLoai;
        this.soLuongTon = soLuongTon;
        this.donViTinh = donViTinh;
        this.donGia = donGia;
        this.hanSuDung = hanSuDung;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getMaNguyenLieu() { return maNguyenLieu; }
    public void setMaNguyenLieu(String maNguyenLieu) { this.maNguyenLieu = maNguyenLieu; }
    public String getTenNguyenLieu() { return tenNguyenLieu; }
    public void setTenNguyenLieu(String tenNguyenLieu) { this.tenNguyenLieu = tenNguyenLieu; }
    public String getPhanLoai() { return phanLoai; }
    public void setPhanLoai(String phanLoai) { this.phanLoai = phanLoai; }
    public float getSoLuongTon() { return soLuongTon; }
    public void setSoLuongTon(float soLuongTon) { this.soLuongTon = soLuongTon; }
    public String getDonViTinh() { return donViTinh; }
    public void setDonViTinh(String donViTinh) { this.donViTinh = donViTinh; }
    public float getDonGia() { return donGia; }
    public void setDonGia(float donGia) { this.donGia = donGia; }
    public Date getHanSuDung() { return hanSuDung; }
    public void setHanSuDung(Date hanSuDung) { this.hanSuDung = hanSuDung; }
}
