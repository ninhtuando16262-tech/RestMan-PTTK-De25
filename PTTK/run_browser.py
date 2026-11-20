import webbrowser
import threading
import time
import uvicorn
from app import app

def open_browser():
    time.sleep(1.2)
    url = "http://localhost:8080"
    print(f"\n[RestMan] Đang mở trình duyệt tại: {url}\n")
    webbrowser.open(url)

if __name__ == '__main__':
    port = 8080
    threading.Thread(target=open_browser, daemon=True).start()
    print("=" * 65)
    print("  HỆ THỐNG QUẢN LÝ NHÀ HÀNG RESTMAN (ĐỀ SỐ 25 - PTTK)")
    print("  Tự động mở trình duyệt web: http://localhost:8080")
    print("=" * 65)
    uvicorn.run("app:app", host="127.0.0.1", port=port, log_level="info")
