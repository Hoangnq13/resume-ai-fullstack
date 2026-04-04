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
      // 🚀 BẮN API LÊN ĐÁM MÂY RENDER GO GO GO!
      const response = await axios.post('https://resume-ai-fullstack-3a0o.onrender.com/api/parse-resume/', formData, {
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