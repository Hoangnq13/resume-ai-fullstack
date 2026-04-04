# BÀI THI TỐT NGHIỆP: QUĂNG HỆ THỐNG LÊN MÂY
# PHASE 3: ĐỘI VƯƠNG MIỆN REACT LÊN VERCEL

Khu vực Backend đã được bảo kê 24/7 bởi Render. Bây giờ là thủ tục cuối cùng: Giao diện React cực phẩm của bạn phải được quăng ra ánh sáng để bất kỳ ai trên thế giới cũng dùng được!

---

## 💻 TASK 1: LIÊN SƠN ĐỈNH VERCEL
1. Bạn hãy vào trang **[Vercel.com](https://vercel.com/)** và đăng nhập bằng tài khoản Github lúc nãy.
2. Bấm vào nút **"Add New Project"** (Thêm dự án mới) siêu to khổng lồ nằm ở trang chủ.
3. Vercel sẽ vác nguyên danh sách các Kho (Repositories) bên Github của bạn sang. Hãy bấm nút **Import** ở cái kho `resume-ai-fullstack` mà hôm nay chúng ta xài.

---

## 💻 TASK 2: CHỈ ĐƯỜNG CHO VERCEL VÀO ĐÚNG HANG
Vì mã nguồn của chúng ta là "Monorepo" (Cả làng ở chung), nên bạn phải dạy thằng Vercel cách chui vào đúng thư mục Frontend. Đừng vội bấm Deploy ngay mà hãy sửa cấu hình sau:

- Mục **Framework Preset:** Vercel quá thông minh nên nó sẽ mặc định tự nhận dạng đây là dự án **Vite**. Bạn cứ giữ nguyên `Vite` nhé.
- Mục **Root Directory:** Bạn nhấp vào nút `Edit` và chọn chuẩn xác thư mục **`frontend_web`**. Xong bấm Continue.

*(Mấy mục Build Command với Output Directory cứ để mặc định cho tụi Vercel nó lo tự động).*

---

## 💻 TASK 3: ẤN NÚT VÀ TẬN HƯỞNG
Chữ **Deploy** màu đen to bự ở dưới cùng. Bấm phát một!!

Vercel sẽ ném bom pháo hoa tưng bừng ăn mừng khi nó Build xong chưa tới 30 giây. 
Và bạn sẽ nhận được một cái tên miền siêu sang chảnh cực xịn (Ví dụ: `resume-ai-fullstack-xxxx.vercel.app`). 

Lấy điện thoại của bạn, mở 4G lên, truy cập vào đường link đó và lấy cái File CV ném vào xem điều kì diệu xảy ra nhé Kỹ Sư! Đừng quên dán đường link Vercel lên đây cho ông giáo nhận xét đồ án tốt nghiệp! 🚀
