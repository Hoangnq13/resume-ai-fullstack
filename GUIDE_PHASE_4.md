# ĐẠI DỰ ÁN BÀI 15: AI RESUME PARSER (PHẦN CUỐI)
# BƯỚC 4: LÊN ĐỒ MẶC ĐẸP (REACT FRONTEND)

Server Backend của ta đã chạy ngầm sừng sững nhưng mắt thường không nhìn thấy được. Khách hàng đâu có biết dùng lệnh Terminal để gửi API? Giai đoạn cuối cùng là dựng lên một khung giao diện Dark Mode cực ngầu để người ta nén file PDF lại và tống sang Server.

---

## 💻 TASK 1: KHỞI TẠO CỖ MÁY VITE REACT
Mình muốn bạn hãy mở thêm **MỘT CÁI TERMINAL MỚI** (Giữ nguyên cái Terminal cũ đang chạy `runserver` cho Backend, đừng tắt nó đi!).

Ở Terminal mới này, hãy chắc chắn bạn đang đứng ở gốc dự án `/home/hoangnq/langchain/15_resume_parser`. Chạy lệnh sau:
```bash
# Sinh ra mã nguồn React
npm create vite@latest frontend_web -- --template react

# Chui vào thư mục web và tải đạn
cd frontend_web
npm install
npm install axios
```

---

## 💻 TASK 2: BIẾN HÌNH NỀN TỐI (DARK MODE)
Mở file `15_resume_parser/frontend_web/src/App.css`, xoá sạch bách toàn bộ bên trong và dán cái file thiết kế UX/UI Premium xịn xò này vào:

```css
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #0f172a;
  color: #f8fafc;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
.app-container {
  width: 90%;
  max-width: 800px;
  background: #1e293b;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.5);
  text-align: center;
}
.title {
  color: #38bdf8;
  font-size: 2.5rem;
  margin-bottom: 5px;
}
.subtitle {
  color: #94a3b8;
  margin-bottom: 30px;
}
.upload-zone {
  border: 2px dashed #475569;
  border-radius: 12px;
  padding: 50px 20px;
  cursor: pointer;
  transition: all 0.3s;
  background: #0f172a;
}
.upload-zone:hover {
  border-color: #38bdf8;
  background: #162032;
}
.file-name {
  color: #4ade80;
  font-weight: bold;
  margin-top: 15px;
}
.btn-submit {
  background: linear-gradient(135deg, #0284c7, #2563eb);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 30px;
  font-size: 1.2rem;
  font-weight: bold;
  margin-top: 25px;
  cursor: pointer;
  transition: transform 0.2s;
  width: 100%;
}
.btn-submit:hover {
  transform: scale(1.02);
}
.btn-submit:disabled {
  background: #475569;
  cursor: not-allowed;
}
/* Card Kết Quả */
.result-card {
  margin-top: 40px;
  background: #0f172a;
  padding: 25px;
  border-radius: 12px;
  text-align: left;
  border-left: 5px solid #38bdf8;
}
.section-title {
  color: #38bdf8;
  border-bottom: 1px solid #334155;
  padding-bottom: 10px;
}
.tag {
  display: inline-block;
  background: #334155;
  padding: 5px 12px;
  border-radius: 20px;
  margin: 5px 5px 0 0;
  font-size: 0.9rem;
}
```

---

## 💻 TASK 3: LOGIC REACT KẾT NỐI BACKEND (MÀN CHÍNH)
Mở file `15_resume_parser/frontend_web/src/App.jsx`, xoá sạch bách và dán cục mìn React này vào (Lưu ý: Mình đã viết sẵn logic dùng Axios để kết nối đập vào cổng `http://127.0.0.1:8000/api/parse-resume/` của Django):

```jsx
import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [errorMsg, setErrorMsg] = useState("")

  const handleFileChange = (e) => {
    if(e.target.files && e.target.files[0]){
      setFile(e.target.files[0])
      setResult(null)
      setErrorMsg("")
    }
  }

  const handleUpload = async () => {
    if (!file) {
      alert("Sếp phải chọn file PDF chứ!")
      return
    }
    
    setLoading(true)
    setErrorMsg("")
    
    // Gói file bỏ vào vali FormData gửi đi
    const formData = new FormData()
    formData.append('pdf_file', file)

    try {
      // 🚀 BẮN API GO GO GO!
      const response = await axios.post('http://127.0.0.1:8000/api/parse-resume/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      setResult(response.data.parsed_data)
      
    } catch (err) {
      setErrorMsg("Ối dồi ôi! Gọi Backend xịt. Cậu xem Server Django chạy chưa?")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <h1 className="title">AI.RESUME.PRO</h1>
      <p className="subtitle">Tuyển Dụng Thần Tốc với Sức Mạnh AI LangChain</p>

      {/* Khu vực Upload */}
      <div className="upload-zone" onClick={() => document.getElementById('fileUpload').click()}>
        <input 
          id="fileUpload" type="file" accept=".pdf" 
          hidden onChange={handleFileChange} 
        />
        <h2>📁 Bấm để Chọn File CV (PDF)</h2>
        {file && <div className="file-name"> Đã chọn: {file.name} </div>}
      </div>

      <button className="btn-submit" onClick={handleUpload} disabled={!file || loading}>
        {loading ? "🤖 AI Đang nhào nặn sấm chớp..." : "🚀 BÓC TÁCH CV TỰ ĐỘNG"}
      </button>
      
      {errorMsg && <p style={{color: '#ef4444', marginTop: 20}}>{errorMsg}</p>}

      {/* Khu vực hiển thị kết quả Trả Về */}
      {result && (
        <div className="result-card">
          <h2 className="section-title">👤 Thông Tin Ứng Viên</h2>
          <p><strong>Họ Tên:</strong> {result.ho_ten}</p>
          <p><strong>Email:</strong> {result.email} | <strong>SĐT:</strong> {result.so_dien_thoai}</p>
          
          <h2 className="section-title" style={{marginTop: 30}}>⚔️ Top Kỹ Năng</h2>
          <div>
            {result.tom_tat_ky_nang && result.tom_tat_ky_nang.map(skill => (
              <span className="tag" key={skill}>{skill}</span>
            ))}
          </div>

          <h2 className="section-title" style={{marginTop: 30}}>🧠 AI Đánh Giá Tổng Quan</h2>
          <p style={{color: '#4ade80', lineHeight: 1.6}}> {result.danh_gia_tong_quan} </p>
          
          <h2 className="section-title" style={{marginTop: 30}}>🏢 Kinh Nghiệm Ngành</h2>
          <ul>
            {result.kinh_nghiem && result.kinh_nghiem.map((kn, idx) => (
             <li key={idx} style={{marginBottom: 10}}>
                <strong>{kn.cong_ty}</strong> - {kn.chuc_vu} <em>({kn.thoi_gian})</em>
             </li> 
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App
```

---

## 🏃 BẬT SERVER FRONTEND VÀ CHIÊM NGƯỠNG ĐẾ CHẾ
Trở lại Terminal của Web:
```bash
npm run dev
```
Giờ thì hãy bôi đen dòng chữ `http://localhost:5173` trên Terminal, click để mở lên trình duyệt. Lấy bừa 1 cái CV của bạn quăng vào, ấn Upload và tận hưởng thành quả đi kỹ sư! Mình chờ báo cáo "Mission Passed" từ bạn đây!!! 🏆
