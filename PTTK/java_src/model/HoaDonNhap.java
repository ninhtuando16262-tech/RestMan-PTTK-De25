package model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class HoaDonNhap implements Serializable {
    private int id;
    private String maHoaDonNhap;
    private Date ngayNhap;
    private NhaCungCap nhaCungCap;
    private NhanVienKho nhanVienKho;
    private float tongTien;
    private String ghiChu;
    private List<HoaDonNhapChiTiet> danhSachChiTiet = new ArrayList<>();

    public HoaDonNhap() {}

    public HoaDonNhap(int id, String maHoaDonNhap, Date ngayNhap, NhaCungCap nhaCungCap, NhanVienKho nhanVienKho, float tongTien, String ghiChu) {
        this.id = id;
        this.maHoaDonNhap = maHoaDonNhap;
        this.ngayNhap = ngayNhap;
        this.nhaCungCap = nhaCungCap;
        this.nhanVienKho = nhanVienKho;
        this.tongTien = tongTien;
        this.ghiChu = ghiChu;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getMaHoaDonNhap() { return maHoaDonNhap; }
    public void setMaHoaDonNhap(String maHoaDonNhap) { this.maHoaDonNhap = maHoaDonNhap; }
    public Date getNgayNhap() { return ngayNhap; }
    public void setNgayNhap(Date ngayNhap) { this.ngayNhap = ngayNhap; }
    public NhaCungCap getNhaCungCap() { return nhaCungCap; }
    public void setNhaCungCap(NhaCungCap nhaCungCap) { this.nhaCungCap = nhaCungCap; }
    public NhanVienKho getNhanVienKho() { return nhanVienKho; }
    public void setNhanVienKho(NhanVienKho nhanVienKho) { this.nhanVienKho = nhanVienKho; }
    public float getTongTien() { return tongTien; }
    public void setTongTien(float tongTien) { this.tongTien = tongTien; }
    public String getGhiChu() { return ghiChu; }
    public void setGhiChu(String ghiChu) { this.ghiChu = ghiChu; }
    public List<HoaDonNhapChiTiet> getDanhSachChiTiet() { return danhSachChiTiet; }
    public void setDanhSachChiTiet(List<HoaDonNhapChiTiet> danhSachChiTiet) { this.danhSachChiTiet = danhSachChiTiet; }
}
