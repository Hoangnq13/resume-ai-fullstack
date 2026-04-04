# BÀI THI TỐT NGHIỆP: QUĂNG HỆ THỐNG LÊN MÂY
# PHASE 2: TREO NÃO BACKEND LÊN ĐÁM MÂY RENDER

Mạch máu Database ở Phase 1 đã thông suốt. Giờ ta sẽ tóm lấy khối óc Django này, quăng nó lên đám mây Render để nó mở cổng chạy 24/7 chờ lệnh từ mọi nơi trên Trái Đất.

---

## 💻 TASK 1: CHUẨN BỊ ĐỒ NGHỀ CHO ĐÁM MÂY
Máy chủ của Render hoàn toàn trần truồng. Nó cần bạn ghi ra 1 danh sách Mua Sắm để nó biết phải cài những thư viện gì.
1. Bạn hãy mở **Thư mục gốc `15_resume_parser`** trong VS Code (Lưu ý là thư mục gốc ở ngoài cùng, không phải thư mục con bên trong đâu nhé!).
2. Cụ thể, bạn tạo file có tên là `requirements.txt` nằm ngay trong lõi của dự án (cùng cấp với thư mục `backend_core` và `frontend_web`), sau đó chép y nguyên danh sách bí mật này vào:
```txt
Django==5.0.3
djangorestframework==3.15.1
django-cors-headers==4.3.1
pypdf==4.1.0
langchain==0.1.13
langchain-google-genai==1.0.1
langchain-community==0.0.29
langchain-core==0.1.33
dj-database-url==2.1.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
python-dotenv==1.0.1
```
*(Gunicorn là cái máy nổ công nghiệp sẽ chạy ngầm thay cho lệnh runserver thủ công).*

---

## 💻 TASK 2: ĐẨY NGUYÊN CỤC CODE LÊN GITHUB
Render không nhận file Zip. Nó chỉ lấy Code từ Github.
1. Bạn tạo 1 tài khoản **[Github.com](https://github.com/)** miễn phí.
2. Tạo 1 cái kho (Repository) mới tên là `resume-ai-fullstack` (để chế độ Public hay Private tùy bạn).
3. (Có thể dùng giao diện VS Code hoặc gõ lệnh) Bắn toàn bộ thư mục `15_resume_parser` này lên cái kho Github đó. 
👉 _Mẹo: Thư mục môi trường ảo `venv` tốn tới mấy trăm MB, đừng có quăng nó lên Github nhé!_

---

## 💻 TASK 3: ĐÁNH THỨC RENDER
1. Vào **[Render.com](https://render.com/)**, kết nối với tài khoản Github bạn vừa tạo.
2. Chọn khu vực **Web Service**, bấm Nút Tạo Mới.
3. Liên kết với kho `resume-ai-fullstack` vừa đẩy lên.
4. Cấu hình các thông số tối quan trọng theo đúng Thần chú sau:
   - Name: `hoangnq-backend-ai` (Đặt gì cũng được)
   - Runtime: `Python 3`
   - Build Command: `cd backend_core && pip install -r ../requirements.txt && python manage.py migrate`
   - Start Command: `cd backend_core && gunicorn backend_core.wsgi:application`
5. Cuộn xuống phần **Environment Variables (Biến môi trường) - RẤT QUAN TRỌNG:**
   - Thêm nút `GEMINI_API_KEY` và dán lại cái key AI của bạn vào. Khúc này mà lười là con AI nó câm điếc ngay!
6. Bấm Lưu và ngồi vểnh râu uống trà xem nó Build.

Nếu nó chạy hiện dòng chữ màu xanh lá báo thành công, và cấp cho bạn 1 đường link (Ví dụ: `https://hoangnq-backend-ai.onrender.com`), hãy gửi cái Link Đám Mây Mới đó lên đây để mình tiếp tục làm phép cho cái Giao Diện React ở Phase 3 đập thẳng vào cái Link đó! 🚀
