package model;

import java.util.Date;

public class TKnhacungcap extends NhaCungCap {
    private Date ngayBatDau;
    private Date ngayKetThuc;
    private float tongSoLuongNhap;
    private int soLanNhap;
    private float tongTienNhap;

    public TKnhacungcap() {
        super();
    }

    public Date getNgayBatDau() { return ngayBatDau; }
    public void setNgayBatDau(Date ngayBatDau) { this.ngayBatDau = ngayBatDau; }
    public Date getNgayKetThuc() { return ngayKetThuc; }
    public void setNgayKetThuc(Date ngayKetThuc) { this.ngayKetThuc = ngayKetThuc; }
    public float getTongSoLuongNhap() { return tongSoLuongNhap; }
    public void setTongSoLuongNhap(float tongSoLuongNhap) { this.tongSoLuongNhap = tongSoLuongNhap; }
    public int getSoLanNhap() { return soLanNhap; }
    public void setSoLanNhap(int soLanNhap) { this.soLanNhap = soLanNhap; }
    public float getTongTienNhap() { return tongTienNhap; }
    public void setTongTienNhap(float tongTienNhap) { this.tongTienNhap = tongTienNhap; }
}
