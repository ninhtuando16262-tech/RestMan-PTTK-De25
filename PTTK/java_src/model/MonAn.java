package model;

import java.io.Serializable;

public class MonAn implements Serializable {
    private int id;
    private String maMon;
    private String tenMon;
    private String loai;
    private String khauPhan;
    private float giaTien;
    private String moTa;
    private String hinhAnh;
    private String trangThai;

    public MonAn() {}

    public MonAn(int id, String maMon, String tenMon, String loai, String khauPhan, float giaTien, String moTa, String hinhAnh, String trangThai) {
        this.id = id;
        this.maMon = maMon;
        this.tenMon = tenMon;
        this.loai = loai;
        this.khauPhan = khauPhan;
        this.giaTien = giaTien;
        this.moTa = moTa;
        this.hinhAnh = hinhAnh;
        this.trangThai = trangThai;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getMaMon() { return maMon; }
    public void setMaMon(String maMon) { this.maMon = maMon; }
    public String getTenMon() { return tenMon; }
    public void setTenMon(String tenMon) { this.tenMon = tenMon; }
    public String getLoai() { return loai; }
    public void setLoai(String loai) { this.loai = loai; }
    public String getKhauPhan() { return khauPhan; }
    public void setKhauPhan(String khauPhan) { this.khauPhan = khauPhan; }
    public float getGiaTien() { return giaTien; }
    public void setGiaTien(float giaTien) { this.giaTien = giaTien; }
    public String getMoTa() { return moTa; }
    public void setMoTa(String moTa) { this.moTa = moTa; }
    public String getHinhAnh() { return hinhAnh; }
    public void setHinhAnh(String hinhAnh) { this.hinhAnh = hinhAnh; }
    public String getTrangThai() { return trangThai; }
    public void setTrangThai(String trangThai) { this.trangThai = trangThai; }
}
