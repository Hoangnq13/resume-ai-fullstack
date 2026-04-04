# ĐẠI DỰ ÁN BÀI 15: AI RESUME PARSER (PHẦN 2)
# BƯỚC 2: TRÁI TIM CỦA ỨNG DỤNG (AI SERVICE)

Bạn đã xuất sắc vượt qua phần khung xương (Database). Bây giờ chúng ta sẽ chế tạo "Bộ Não" cho hệ thống, kết hợp trọn vẹn sức mạnh của Bài 3 (Prompt), Bài 5 (JSON Parser), và Bài 8 (PDF Loader).

Nhiệm vụ của phần này là nhận 1 file CV PDF được gửi lên, chép chữ ra, cho vào Não AI nhào nặn theo khuôn JSON, và ném kết quả về cho hệ thống.

---

## 💻 TASK 1: KHAI BÁO CẤU TRÚC JSON MONG MUỐN BẰNG PYDANTIC
Khác với Bài 5 đôi khi AI nặn JSON bị xô lệch, làm dự án thật ta phải dùng công cụ "Ép khuôn" chuẩn mực của Python tên là Pydantic. 
1. Vào thư mục `15_resume_parser/backend_core/parser_app/`.
2. Tạo thư mục con tên là `services` và tiếp tục tạo một file `__init__.py` thả rỗng ở trong đó.
3. Cũng trong thư mục `services` đó, tạo tiếp file `ai_service.py` và bơm nội dung cực mạnh sau vào:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

# Khuôn Hộp Đựng Dữ Liệu
class KinhNghiem(BaseModel):
    cong_ty: str = Field(description="Tên công ty ứng viên từng làm việc")
    chuc_vu: str = Field(description="Chức danh")
    thoi_gian: str = Field(description="Thời gian làm việc")

class HocVan(BaseModel):
    truong: str = Field(description="Tên trường đại học / cao đẳng")
    chuyen_nganh: str = Field(description="Chuyên ngành đại học")
    nam_tot_nghiep: str = Field(description="Năm tốt nghiệp")

# KHUÔN CHÍNH (Sẽ lưu vào Database)
class ResumeSchema(BaseModel):
    ho_ten: str = Field(description="Họ và tên đầy đủ của ứng viên")
    email: str = Field(description="Địa chỉ email cá nhân")
    so_dien_thoai: str = Field(description="Số điện thoại cá nhân")
    tom_tat_ky_nang: List[str] = Field(description="Trích xuất danh sách ngắn gọn 5-7 kỹ năng mạnh nhất (ví dụ: Python, React, SQL...)")
    kinh_nghiem: List[KinhNghiem] = Field(description="Lịch sử làm việc")
    hoc_van: List[HocVan] = Field(description="Lịch sử học vấn")
    danh_gia_tong_quan: str = Field(description="Chỉ viết 2 câu: Tóm tắt điểm mạnh yếu của CV này")
```

---

## 💻 TASK 2: VIẾT HÀM XỬ LÝ (CORE PIPELINE)
Bên dưới file `ai_service.py` mà bạn vừa khai báo Pydantic ở trên, bạn THÊM ĐOẠN CODE NÀY vào cuối file để tạo hàm Pipeline Langchain:

```python
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import PyPDFLoader

# Cái này để nó tìm thấy file .env ở thư mục ông nội của nó
load_dotenv(dotenv_path='../../.env')

def parse_resume_to_json(pdf_file_path: str):
    """
    Hàm này nhận đầu vào là file PDF lưu trên ổ cứng mạng,
    đọc nó ra rồi ép AI trả về chuẩn JSON đã định nghĩa.
    """
    # Bước 1: Máy chém PDF (Đọc Text)
    loader = PyPDFLoader(pdf_file_path)
    vi_danh_text = loader.load()
    noi_dung_cv = "\\n".join([page.page_content for page in vi_danh_text])

    # Bước 2: Setup Phép Thuật (LLM & Khuôn JSON)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0) # Temp=0 để AI KHÔNG ĐƯỢC CHẾ THÊM, chỉ BÓC TÁCH.
    parser = JsonOutputParser(pydantic_object=ResumeSchema)

    # Bước 3: Đe doạ AI
    mau_lenh = """
    Bạn là một siêu AI phân tích hồ sơ ứng viên (Resume Parser) cho một công ty toàn cầu.
    Nhiệm vụ của bạn là đọc toàn bộ Mớ chữ lộn xộn dưới đây và lọc ra các thông tin theo đúng Format được yêu cầu.
    Nếu ứng viên không viết nội dung nào đó, hãy để "Không có".
    
    ĐÂY LÀ MỚ CHỮ BẠN CẦN ĐỌC KỸ:
    {noi_dung_cv}
    
    YÊU CẦU ĐẦU RA BẮT BUỘC:
    {format_instructions}
    """
    prompt = PromptTemplate(
        template=mau_lenh,
        input_variables=["noi_dung_cv"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # Bước 4: Vòng Nối Pipeline Đỉnh Cao
    doan_tau = prompt | llm | parser

    # Bước 5: Bấm Nút Lụm Tiền
    print("\\n[AI_SERVICE] Bắt đầu bật Haki Quan Sát đọc CV...")
    ket_qua = doan_tau.invoke({"noi_dung_cv": noi_dung_cv})
    print("[AI_SERVICE] Done! Đã rọc xong CV ra JSON siêu chuẩn!")
    
    return ket_qua
```

---

## 🏃 HOÀN THIỆN PHASE 2
Xong file này là chúng ta đã giải quyết dứt điểm 80% độ khó của toàn bộ phần Backend. Bạn lưu file `ai_service.py` lại. 

Chỉ cần gõ theo hướng dẫn, chuẩn bị sẵn sàng, và comment cho mình để mình tung ra phần hấp dẫn nhất: **PHASE 3: Mở một đường Link API để cho màn hình Frontend React gọi tới!** 🚀
