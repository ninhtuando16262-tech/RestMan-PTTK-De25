@echo off
chcp 65001 > nul
title Hệ Thống Quản Lý Nhà Hàng RestMan - Đề 25
echo ====================================================================
echo        HỆ THỐNG QUẢN LÝ NHÀ HÀNG RESTMAN (ĐỀ SỐ 25 - PTTK)
echo ====================================================================
echo Đang khởi tạo cơ sở dữ liệu và khởi động Web Server...
python database/init_db.py
echo.
echo Khởi chạy Web Server tại http://localhost:8080 ...
python run_browser.py
pause
