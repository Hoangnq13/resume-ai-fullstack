# ĐẠI DỰ ÁN BÀI 15: AI RESUME PARSER (PHẦN 3)
# BƯỚC 3: MỞ CỔNG GIAO DỊCH (REST API) VÀ DATABASE

Bộ não trâu bò `ai_service.py` đã sẵn sàng súng đạn. Vấn đề là hiện tại nó đang bị nhốt kín dưới lòng đất Backend.
Nhiệm vụ của Phase 3 là: Xây dựng một cánh cổng (API endpoint) để Website Frontend Mở Cửa -> Nhét file PDF vào -> Cổng tự động đưa cho AI xử lý -> Lấy kết quả lưu thẳng vào kho Database (Postgres/SQLite) -> Ném trả dữ liệu báo cáo ra ngoài Website.

---

## 💻 TASK 1: KHAI BÁO BỘ ĐÓNG GÓI DỮ LIỆU (SERIALIZERS)
Bạn tạo mới một file tại `15_resume_parser/backend_core/parser_app/serializers.py` và dán cục code này vào:

```python
from rest_framework import serializers
from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'  # Yêu cầu DRF chuyển toàn bộ cột trong Bảng Candidate thành JSON gửi về Client
```

---

## 💻 TASK 2: VIẾT LOGIC GÁC CỔNG API (VIEWS)
Mở file `15_resume_parser/backend_core/parser_app/views.py` ra và hất sạch cái cũ đi, thay bằng cục Code API tuyệt đỉnh này:

```python
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .models import Candidate
from .serializers import CandidateSerializer
from .services.ai_service import parse_resume_to_json

@api_view(['POST'])
@parser_classes([MultiPartParser])
def parse_resume_api(request):
    # 1. Bắt file từ client (Màn hình Web React) gửi qua mạng
    file_obj = request.FILES.get('pdf_file')
    if not file_obj:
        return Response({"error": "Sếp ơi chưa đính kèm file PDF!"}, status=400)
    
    # 2. Ra lệnh cho CSDL tạo một row mới giữ chỗ và CẤT FILE DỰ PHÒNG tránh mất mát
    candidate = Candidate.objects.create(pdf_file=file_obj)
    
    # 3. Lấy đường dẫn file vừa cất trên ổ cứng
    file_path = candidate.pdf_file.path
    
    try:
        # 4. Kêu AI CÀO FILE PDF ĐÓ! (Trái tim Bài 2 sẽ đập ở đây)
        json_data = parse_resume_to_json(file_path)
        
        # 5. Lưu cục JSON xịn xò mà AI vừa vẽ ra vào CSDL
        candidate.ho_ten = json_data.get('ho_ten', '')
        candidate.email = json_data.get('email', '')
        candidate.so_dien_thoai = json_data.get('so_dien_thoai', '')
        candidate.parsed_data = json_data # Nhét trọn vẹn JSON gồm Kỹ năng, Học vấn vào Cột đặc biệt
        candidate.save()
        
        # 6. Biến row CSDL đó thành Text JSON để gửi ra ngoài cho React vẽ Màn hình
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_candidates_api(request):
    """Lấy danh sách tất cả CV đã từng băm ra để hiển thị trang chủ"""
    candidates = Candidate.objects.all().order_by('-created_at')
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)
```

---

## 💻 TASK 3: TẠO BẢN ĐỒ ĐƯỜNG DẪN MẠNG (URLS)
Bây giờ phải vẽ đường cho React gọi tới đúng cái hàm `parse_resume_api` kia.

**1. Trong `parser_app/urls.py`:** 
Tạo file `15_resume_parser/backend_core/parser_app/urls.py` rỗng và chép đoạn này vào:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('parse-resume/', views.parse_resume_api, name='parse_resume_api'),
    path('candidates/', views.get_candidates_api, name='get_candidates_api'),
]
```

**2. Đấu nối nó vào Mạng lưới Toàn cục (`backend_core/urls.py`):**
Mở file `15_resume_parser/backend_core/backend_core/urls.py` và sửa thành như sau:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('parser_app.urls')), # Cánh cổng API bắt đầu được mở 
]
```

---

## 🏃 BƯỚC KIỂM TRA CHỐT HẠ PHASE 3
Mọi code Backend Server đã hoàn tất!
Bạn bật Terminal ở thư mục `15_resume_parser/backend_core`, gõ lệnh kích hoạt server chấn động thế giới:
```bash
python manage.py runserver
```
Và báo lại cho mình nếu Terminal của bạn hiện Cảnh báo màu Xanh rực rỡ bảo là Server đang quay đều tại cổng `http://127.0.0.1:8000/`. Mình sẽ tung giáo án Phase Cuối Cùng: Mở Giao Diện React Tải File Tuyệt Đẹp nhé! 🚀
