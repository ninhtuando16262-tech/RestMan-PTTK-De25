# ====================================================================
# HỆ THỐNG QUẢN LÝ NHÀ HÀNG RESTMAN (ĐỀ SỐ 25 - PTTK)
# Web Application Server: Starlette + Jinja2 + SQLite3
# ====================================================================

import os
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from models.dao import (
    MonAnDAO, TKnhacungcapDAO, HoaDonNhapDAO, HoaDonNhapChiTietDAO, ThanhVienDAO
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

templates = Jinja2Templates(directory=TEMPLATES_DIR)

def render(request, template_name, context=None):
    """Helper render tương thích với Starlette 1.x+"""
    ctx = context or {}
    return templates.TemplateResponse(request=request, name=template_name, context=ctx)

# Khởi tạo các DAO theo kiến trúc PTTK
monan_dao = MonAnDAO()
tk_ncc_dao = TKnhacungcapDAO()
hd_nhap_dao = HoaDonNhapDAO()
hd_nhap_ct_dao = HoaDonNhapChiTietDAO()
thanhvien_dao = ThanhVienDAO()

def get_current_user(request):
    """Lấy thông tin người dùng hiện tại từ session hoặc mặc định"""
    user_data = request.session.get('user')
    if user_data:
        class SessionUser:
            def __init__(self, d):
                self.__dict__.update(d)
        return SessionUser(user_data)
    return None

# ==================== CONTROLLERS / ROUTE HANDLERS ====================

async def index(request):
    """Trang chủ: Điều hướng theo vai trò hoặc vào đăng nhập"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url='/login', status_code=303)
    if user.vaitro == 'QuanLy':
        return RedirectResponse(url='/quan-ly', status_code=303)
    return RedirectResponse(url='/khach-hang', status_code=303)

async def login_view(request):
    """Giao diện đăng nhập hệ thống"""
    if request.method == 'POST':
        form = await request.form()
        tendangnhap = form.get('tendangnhap', '').strip()
        matkhau = form.get('matkhau', '').strip()
        
        user = thanhvien_dao.kiemTraDangNhap(tendangnhap, matkhau)
        if user:
            request.session['user'] = {
                'id': user.id,
                'ten': user.ten,
                'tendangnhap': user.tendangnhap,
                'vaitro': user.vaitro,
                'email': user.email,
                'sdt': user.sdt,
                'diachi': user.diachi
            }
            if user.vaitro == 'QuanLy':
                return RedirectResponse(url='/quan-ly', status_code=303)
            return RedirectResponse(url='/khach-hang', status_code=303)
        else:
            return render(request, 'login.html', {
                'error': 'Tên đăng nhập hoặc mật khẩu không chính xác!',
                'tendangnhap': tendangnhap,
                'user': None
            })
            
    user = get_current_user(request)
    return render(request, 'login.html', {
        'user': user
    })

async def login_as(request):
    """Đăng nhập nhanh 1-click theo vai trò (Dành cho việc chấm bài & trải nghiệm nhanh)"""
    role = request.query_params.get('role', 'KhachHang')
    role_accounts = {
        'KhachHang': ('khachhang1', '123456'),
        'QuanLy': ('quanly1', '123456'),
        'NhanVienKho': ('nhanvienkho1', '123456'),
        'NhanVienBanHang': ('nhanvienbanhang1', '123456')
    }
    acc, pwd = role_accounts.get(role, ('khachhang1', '123456'))
    user = thanhvien_dao.kiemTraDangNhap(acc, pwd)
    if user:
        request.session['user'] = {
            'id': user.id,
            'ten': user.ten,
            'tendangnhap': user.tendangnhap,
            'vaitro': user.vaitro,
            'email': user.email,
            'sdt': user.sdt,
            'diachi': user.diachi
        }
        if user.vaitro == 'QuanLy':
            return RedirectResponse(url='/quan-ly', status_code=303)
        return RedirectResponse(url='/khach-hang', status_code=303)
    return RedirectResponse(url='/login', status_code=303)

async def logout_view(request):
    """Đăng xuất"""
    request.session.clear()
    return RedirectResponse(url='/login', status_code=303)

# ==================== MODULE 1: KHÁCH HÀNG TÌM KIẾM MÓN ĂN ====================

async def gd_chinh_kh(request):
    """Lớp Boundary GDChinhKH: Trang chủ khách hàng"""
    user = get_current_user(request)
    if not user:
        # Nếu chưa đăng nhập, tự động gán tài khoản khách hàng mẫu
        user = thanhvien_dao.kiemTraDangNhap('khachhang1', '123456')
        request.session['user'] = user.__dict__

    return render(request, 'gd_chinh_kh.html', {
        'user': user,
        'active_page': 'gd_chinh_kh'
    })

async def gd_thong_tin_mon_an(request):
    """
    Lớp Boundary GDThongTinMonAn:
    Xử lý tìm kiếm món ăn theo từ khóa, gọi MonAnDAO.timKiemMonan(tukhoa)
    """
    user = get_current_user(request)
    tukhoa = request.query_params.get('inTukhoa', '').strip()
    
    # Gọi hàm xử lý dưới hệ thống: timKiemMonan()
    danhsach_mon = monan_dao.timKiemMonan(tukhoa)

    return render(request, 'gd_thong_tin_mon_an.html', {
        'user': user,
        'tukhoa': tukhoa,
        'danhsach_mon': danhsach_mon,
        'active_page': 'gd_thong_tin_mon_an'
    })

async def gd_thong_tin_chi_tiet(request):
    """
    Lớp Boundary GDThongTinChiTiet:
    Hiển thị thông tin chi tiết món ăn, gọi MonAnDAO.getChitietMonan(id)
    """
    user = get_current_user(request)
    mon_id = request.query_params.get('id')
    
    if not mon_id:
        return RedirectResponse(url='/tim-kiem-mon-an', status_code=303)
        
    monan = monan_dao.getChitietMonan(int(mon_id))
    if not monan:
        return RedirectResponse(url='/tim-kiem-mon-an', status_code=303)

    return render(request, 'gd_thong_tin_chi_tiet.html', {
        'user': user,
        'monan': monan,
        'active_page': 'gd_thong_tin_mon_an'
    })

# ==================== MODULE 2: THỐNG KÊ NHÀ CUNG CẤP THEO LƯỢNG NHẬP ====================

async def gd_chinh_ql(request):
    """Lớp Boundary GDChinhQL: Bàn làm việc Quản lý"""
    user = get_current_user(request)
    if not user:
        user = thanhvien_dao.kiemTraDangNhap('quanly1', '123456')
        request.session['user'] = user.__dict__

    return render(request, 'gd_chinh_ql.html', {
        'user': user,
        'active_page': 'gd_chinh_ql'
    })

async def gd_chon_thong_ke(request):
    """Lớp Boundary GDChonThongKe: Chọn loại báo cáo thống kê"""
    user = get_current_user(request)
    return render(request, 'gd_chon_thong_ke.html', {
        'user': user,
        'active_page': 'gd_chon_thong_ke'
    })

async def gd_tk_nha_cung_cap(request):
    """
    Lớp Boundary GDTKNhaCungCap:
    Thống kê nhà cung cấp theo lượng nhập trong khoảng thời gian [ngaybatdau, ngayketthuc]
    Gọi phương thức TKnhacungcapDAO.getTKNhaCungCap()
    """
    user = get_current_user(request)
    ngaybatdau = request.query_params.get('inNgaybatdau', '').strip()
    ngayketthuc = request.query_params.get('inNgayketthuc', '').strip()
    sub_xem = request.query_params.get('subXemthongke')
    
    danhsach_ncc = []
    error_message = None
    has_searched = False
    
    # Nếu người dùng đã nhấn nút Xem thống kê hoặc truyền tham số ngày
    if sub_xem or (ngaybatdau and ngayketthuc):
        has_searched = True
        try:
            danhsach_ncc = tk_ncc_dao.getTKNhaCungCap(ngaybatdau, ngayketthuc)
        except ValueError as e:
            error_message = str(e)
            danhsach_ncc = []

    return render(request, 'gd_tk_nha_cung_cap.html', {
        'user': user,
        'ngaybatdau': ngaybatdau,
        'ngayketthuc': ngayketthuc,
        'has_searched': has_searched,
        'error_message': error_message,
        'danhsach_ncc': danhsach_ncc,
        'active_page': 'gd_tk_nha_cung_cap'
    })

async def gd_chi_tiet_lan_nhap(request):
    """
    Lớp Boundary GDChiTietLanNhapNCC:
    Lấy danh sách các lần nhập nguyên liệu của nhà cung cấp đã chọn
    Gọi phương thức HoaDonNhapDAO.getDSLanNhap(id_ncc, ngaybatdau, ngayketthuc)
    """
    user = get_current_user(request)
    id_ncc = request.query_params.get('id_ncc')
    ngaybatdau = request.query_params.get('ngaybatdau', '')
    ngayketthuc = request.query_params.get('ngayketthuc', '')
    
    if not id_ncc:
        return RedirectResponse(url='/thong-ke-nha-cung-cap', status_code=303)
        
    ncc, danhsach_lannhap = hd_nhap_dao.getDSLanNhap(int(id_ncc), ngaybatdau, ngayketthuc)

    return render(request, 'gd_chi_tiet_lan_nhap.html', {
        'user': user,
        'ncc': ncc,
        'danhsach_lannhap': danhsach_lannhap,
        'ngaybatdau': ngaybatdau,
        'ngayketthuc': ngayketthuc,
        'active_page': 'gd_tk_nha_cung_cap'
    })

async def gd_hoa_don_nhap(request):
    """
    Lớp Boundary GDHoaDonNhap:
    Hiển thị thông tin hóa đơn nhập và danh sách chi tiết nguyên liệu nhập
    Gọi phương thức HoaDonNhapChiTietDAO.getChiTietHoaDonNhap(id_hd)
    """
    user = get_current_user(request)
    id_hd = request.query_params.get('id_hd')
    id_ncc = request.query_params.get('id_ncc', '')
    ngaybatdau = request.query_params.get('ngaybatdau', '')
    ngayketthuc = request.query_params.get('ngayketthuc', '')
    
    if not id_hd:
        return RedirectResponse(url='/thong-ke-nha-cung-cap', status_code=303)
        
    hoadon = hd_nhap_ct_dao.getChiTietHoaDonNhap(int(id_hd))
    if not hoadon:
        return RedirectResponse(url='/thong-ke-nha-cung-cap', status_code=303)

    return render(request, 'gd_hoa_don_nhap.html', {
        'user': user,
        'hoadon': hoadon,
        'id_ncc': id_ncc,
        'ngaybatdau': ngaybatdau,
        'ngayketthuc': ngayketthuc,
        'active_page': 'gd_tk_nha_cung_cap'
    })

# Cấu hình danh sách Routes
routes = [
    Route('/', index, methods=['GET']),
    Route('/login', login_view, methods=['GET', 'POST']),
    Route('/login-as', login_as, methods=['GET']),
    Route('/logout', logout_view, methods=['GET']),
    
    # Module 1
    Route('/khach-hang', gd_chinh_kh, methods=['GET']),
    Route('/tim-kiem-mon-an', gd_thong_tin_mon_an, methods=['GET']),
    Route('/chi-tiet-mon-an', gd_thong_tin_chi_tiet, methods=['GET']),
    
    # Module 2
    Route('/quan-ly', gd_chinh_ql, methods=['GET']),
    Route('/bao-cao-thong-ke', gd_chon_thong_ke, methods=['GET']),
    Route('/thong-ke-nha-cung-cap', gd_tk_nha_cung_cap, methods=['GET']),
    Route('/chi-tiet-lan-nhap', gd_chi_tiet_lan_nhap, methods=['GET']),
    Route('/hoa-don-nhap', gd_hoa_don_nhap, methods=['GET']),
    
    # Static files
    Mount('/static', app=StaticFiles(directory=STATIC_DIR), name='static')
]

# Thêm middleware Session để lưu phiên đăng nhập
middleware = [
    Middleware(SessionMiddleware, secret_key="restman-pttk-secret-key-2026")
]

app = Starlette(debug=True, routes=routes, middleware=middleware)

if __name__ == '__main__':
    port = 8080
    print("=" * 60)
    print("  HỆ THỐNG QUẢN LÝ NHÀ HÀNG RESTMAN (ĐỀ SỐ 25 - PTTK)")
    print(f"  Web Server đang chạy tại: http://localhost:{port}")
    print(f"  - Module 1 (Khách hàng):  http://localhost:{port}/khach-hang")
    print(f"  - Module 2 (Quản lý):     http://localhost:{port}/quan-ly")
    print("=" * 60)
    uvicorn.run("app:app", host="127.0.0.1", port=port, log_level="info", reload=False)
