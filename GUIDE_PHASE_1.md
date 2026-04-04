# ĐẠI DỰ ÁN BÀI 15: AI RESUME PARSER (PHẦN 1)
# BƯỚC 1: KHỞI TẠO DJANGO VÀ CƠ SỞ DỮ LIỆU

Chào mừng bạn đến với mô phỏng quy trình thăng cấp làm Kỹ sư Fullstack AI. Mình rất trân trọng tinh thần muốn "tự tay nhúng chàm" của bạn, đó mới là cách học để nhớ suốt đời!

Dự án này rất đồ sộ, vì vậy mình đã rã nó ra thành các Phase (Giai đoạn) nhỏ. Gặp lỗi ở đâu chúng ta sẽ cùng dừng lại sửa tận gốc ở đó.

---

## 💻 TASK 1: CÀI ĐẶT KIẾM VÀ GIÁP CHO BACKEND
Django là một khung xương Web cực lớn. Ta cần cài nó cùng với gói làm API `djangorestframework`, và cài sẵn công cụ đọc file PDF `pypdf`.

Mở Terminal của bạn (đảm bảo đang ở trong chữ `(venv)` xanh rờn), chạy lệnh sau để tải đạn:
```bash
pip install django djangorestframework django-cors-headers pypdf
```

---

## 💻 TASK 2: XÂY MÓNG NHÀ DJANGO PROJECT
Chạy liên tiếp 3 lệnh sau để khởi tạo thư mục và sinh code mặc định của Django:

```bash
# 1. Tạo thư mục tổng của dự án Resume AI
mkdir 15_resume_parser
cd 15_resume_parser

# 2. Sinh ra mã nguồn cấu hình lõi (Đặt tên là backend_core)
django-admin startproject backend_core .

# 3. Tạo một cái App con tên là parser_app (Để chuyên bóc tách CV)
python manage.py startapp parser_app
```

---

## 💻 TASK 3: ĐĂNG KÝ APP VÀ CẤU HÌNH BẢO MẬT
Bạn mở file `15_resume_parser/backend_core/settings.py` ra và sửa lại danh sách `INSTALLED_APPS` (ở loanh quanh dòng 33), hãy thò thêm 3 cái tên này vào cuối danh sách:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # --- Code bạn tự thêm vào đây ---
    'rest_framework',      # Kích hoạt gói làm API
    'corsheaders',         # Cho phép Frontend React gọi API không bị chặn
    'parser_app',          # Kích hoạt cái thư mục parser_app ta vừa tạo lúc nãy
]
```

Và khai báo thư mục lưu file PDF. Cuộn hẳn xuống **DƯỚI CÙNG** của file `settings.py` và dán thêm 2 dòng này vô:
```python
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

## 💻 TASK 4: THIẾT KẾ DATABASE LƯU CV (MODELS)
Đây là bước trả lời cho câu hỏi lưu JSON của bạn lúc nãy.
Bạn mở file `15_resume_parser/parser_app/models.py` ra, viết thiết kế cái Bảng `Candidate` bằng Python như sau:

```python
from django.db import models

class Candidate(models.Model):
    ho_ten = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    so_dien_thoai = models.CharField(max_length=20, null=True, blank=True)
    
    # Chỗ này lưu trữ file PDF do ứng viên up lên
    pdf_file = models.FileField(upload_to='resumes/')
    
    # VIP - Nơi giấu cục Vàng JSON phân tích ra từ AI
    parsed_data = models.JSONField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ho_ten or "Chưa rõ tên"
```

---

## 🏃 BƯỚC KIỂM TRA CUỐI CÙNG CHỐT PHASE 1
Một khi bạn đã thiết kế xong Bảng dữ liệu thì bạn phải yêu cầu Django "Xây gạch" vào CSDL SQLite bằng 2 lệnh quen thuộc. **Nhớ là Terminal của bạn phải đang đứng ở thư mục `15_resume_parser` mới gõ được lệnh `manage.py` nhé:**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Báo cáo cho mình:** Cài đặt mọi thứ, sửa code như mình chỉ xong. Nếu bạn chạy ra dòng chữ màu xanh `Applying parser_app.0001_initial... OK` thì tức là CSDL đã xây xong móng. Cứ comment mình biết để mình tung giáo án làm Task 5 (Đưa AI Gemini vào mổ xẻ) nhé! 🚀
