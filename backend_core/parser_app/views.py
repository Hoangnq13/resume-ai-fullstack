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



