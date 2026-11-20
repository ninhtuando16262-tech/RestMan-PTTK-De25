package model;

import java.io.Serializable;

public class HoaDonNhapChiTiet implements Serializable {
    private int id;
    private int idHoaDonNhap;
    private NguyenLieu nguyenLieu;
    private float soLuong;
    private float donGiaNhap;
    private float thanhTien;

    public HoaDonNhapChiTiet() {}

    public HoaDonNhapChiTiet(int id, int idHoaDonNhap, NguyenLieu nguyenLieu, float soLuong, float donGiaNhap, float thanhTien) {
        this.id = id;
        this.idHoaDonNhap = idHoaDonNhap;
        this.nguyenLieu = nguyenLieu;
        this.soLuong = soLuong;
        this.donGiaNhap = donGiaNhap;
        this.thanhTien = thanhTien;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public int getIdHoaDonNhap() { return idHoaDonNhap; }
    public void setIdHoaDonNhap(int idHoaDonNhap) { this.idHoaDonNhap = idHoaDonNhap; }
    public NguyenLieu getNguyenLieu() { return nguyenLieu; }
    public void setNguyenLieu(NguyenLieu nguyenLieu) { this.nguyenLieu = nguyenLieu; }
    public float getSoLuong() { return soLuong; }
    public void setSoLuong(float soLuong) { this.soLuong = soLuong; }
    public float getDonGiaNhap() { return donGiaNhap; }
    public void setDonGiaNhap(float donGiaNhap) { this.donGiaNhap = donGiaNhap; }
    public float getThanhTien() { return thanhTien; }
    public void setThanhTien(float thanhTien) { this.thanhTien = thanhTien; }
}
