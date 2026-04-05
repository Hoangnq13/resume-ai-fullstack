from pydantic import BaseModel, Field
from typing import List, Optional

class KinhNghiem(BaseModel):
    cong_ty: str = Field(description="Tên Công Ty ứng viên từng làm")
    chuc_vu: str = Field(description="Chức danh")
    thoi_gian: str = Field(description="Thời gian làm việc")

class HocVan(BaseModel):
    truong: str = Field(description="Tên trường đại học / cao đẳng")
    chuyen_nganh: str = Field(description="Chuyên ngành đại học")
    nam_tot_nghiep: str = Field(description="Năm tốt nghiệp")

class ResumeSchema(BaseModel):
    ho_ten: str = Field(description="Họ và tên đầy đủ của ứng viên")
    email: str = Field(description="Địa chỉ email cá nhân")
    so_dien_thoai: str = Field(description="Số điện thoại cá nhân")
    tom_tat_ky_nang: List[str] = Field(description="Trích xuất danh sách ngắn gọn 5-7 kỹ năng mạnh nhất (ví dụ: Python, React, SQL...)")
    kinh_nghiem: List[KinhNghiem] = Field(description="Lịch sử làm việc")
    hoc_van: List[HocVan] = Field(description="Lịch sử học vấn")
    danh_gia_tong_quan: str = Field(description="Chỉ viết 2 câu: Tóm tắt điểm mạnh yếu của CV này")

import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import PyPDFLoader

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
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0) # Temp=0 để AI KHÔNG ĐƯỢC CHẾ THÊM, chỉ BÓC TÁCH.
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