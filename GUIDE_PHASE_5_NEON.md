# BÀI THI TỐT NGHIỆP: QUĂNG HỆ THỐNG LÊN MÂY
# PHASE 1: CHUYỂN NHÀ LÊN NGÂN HÀNG NEONDB

Để Backend "bất tử" dù ở trên máy của bạn hay trên Mỹ, chúng ta phải phẫu thuật cắt bỏ quả tim máu `sqlite3` cục bộ và móc nó lên hệ thống tĩnh mạch trên Đám Mây tên là NeonDB.

---

## 💻 TASK 1: ĐĂNG KÝ KÉT SẮT MIỄN PHÍ TẠI NEON
1. Mở Trình duyệt, vào trang Web: **[https://neon.tech/](https://neon.tech/)**
2. Bấm Nút **Sign up** và Đăng nhập tẹt ga bằng nút `Log in with Google`.
3. Bấm Tạo Project, cứ tự tin để tên project là `   `. (Chọn Vùng Server là AWS US East cho mạnh hoặc Singapore nếu có).
4. Sẽ hiện ra 1 cái bảng "Connection Details". 
5. Bạn để ý cái chuỗi mã dài ngoằng kiểu như vầy: `postgresql://hoangnq:xxxx@ep-dawn-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`
6. Bấm Copy cái chuỗi Dây Chuyền Huyết Mạch cứng đó lại!!!

---

## 💻 TASK 2: NẠP ĐẠN CHO PYTHON ĐỌC POSTGRES
PostgresSQL là đồ chơi xịn, xịn hơn cái Sqlite3 gốc nên Python cần thêm công cụ cạy cửa.

Bạn mở **Terminal mới (đã gõ lệnh source venv đầy đủ)** tại thư mục `15_resume_parser/backend_core`:
```bash
pip install dj-database-url psycopg2-binary
```

---

## 💻 TASK 3: PHẪU THUẬT TIM CỦA DJANGO (SETTINGS.PY)
Bạn mở file `15_resume_parser/backend_core/backend_core/settings.py` ra.

Lèo tới dòng **78**, xóa sạch cái khối `DATABASES = { 'default': { ... } }` vuông vức đấy đi.
Bơm con tim mới này vào thay thế:

```python
import dj_database_url

# Đây là chuỗi bạn copy từ Neon Lúc Nãy
# LƯU Ý: Phải Bỏ mã Copy vào trong ngoặc Kép " "
NEON_DB_URL = "DÁN_CÁI_MÃ_DÀI_NGOẰNG_COPY_TRÊN_NEON_VÀO_ĐÂY"

DATABASES = {
    'default': dj_database_url.config(
        default=NEON_DB_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

---

## 💻 TASK 4: KHỞI TẠO LẠI TOÀN BỘ CSDL LÊN MÂY MỸ
Giờ thì Server Django của bạn đã kết nối đụng nóc tới máy chủ Cloud bên Mỹ (Của tụi Neon). Toàn bộ dữ liệu trống trơn vì cái Mây này là rỗng tuếch.

Hãy bắt Django truyền lệnh "Xây Bảng cấu trúc Data" từ Mỹ về máy tính của bạn bằng lệnh kinh điển:
```bash
python manage.py migrate
```

> ⚠️ **Chú ý:** Nếu lệnh này chạy thành công xuất hiện một nùi chữ `Applying... OK`, tức là Đám Mây Postgres của bạn ở Mỹ đã chính thức có Bảng Candidate! Kể từ giây phút này, vứt Django ở đâu cũng đều moi được dữ liệu.

Báo tin vui lại cho mình nếu lệnh chạy xong không báo màu Đỏ nhé! 🚀
