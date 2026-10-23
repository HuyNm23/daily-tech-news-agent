# 📰 Daily Tech News AI Agent

Một trợ lý **AI Agent tự chủ** được thiết kế siêu nhẹ, chuyên tự động đi săn lùng tin tức công nghệ từ các nguồn hàng đầu (VnExpress Số Hóa, Báo Tuổi Trẻ, Hacker News, TechCrunch), tự động tư duy, lọc bài hot, tóm tắt và xuất báo cáo hàng ngày.

---

## ✨ Điểm Nổi Bật
1. **Siêu nhẹ & Tiết kiệm tài nguyên:**
   - Không chạy ngầm ngốn RAM.
   - Dung lượng toàn bộ project chưa tới 1 MB.
   - Sử dụng thư viện chuẩn của Python, chạy nhanh như chớp (chỉ mất ~3 giây).
2. **Không bắt buộc có API Key (Chạy Offline 100%):**
   - Có sẵn thuật toán phân loại & lọc tin thông minh mà không tốn một xu phí API.
   - Nếu bạn muốn tóm tắt sâu sắc hơn, chỉ cần điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) vào file `.env`.
3. **Đa dạng hình thức báo cáo:**
   - Tự động xuất ra file **Markdown (`.md`)** để xem tiện lợi ngay trong VS Code.
   - Tự động xuất ra giao diện **HTML Web (Dark Mode)** đẹp mắt, mở bằng bất kỳ trình duyệt nào.
   - Tùy chọn gửi tin tóm tắt qua **Telegram**.

---

## 🚀 Cách Mở Trong VS Code & Chạy

### Cách 1: Mở thư mục này bằng VS Code
Trong terminal hoặc PowerShell, gõ:
```bash
code "C:\Users\Admin\.gemini\antigravity\scratch\daily_news_agent"
```

### Cách 2: Cài đặt thư viện (Chỉ mất 2 giây)
```bash
cd "C:\Users\Admin\.gemini\antigravity\scratch\daily_news_agent"
pip install -r requirements.txt
```
*(Nếu chưa cài `pip install`, chương trình vẫn chạy được bình thường bằng thư viện có sẵn của Python!)*

### Cách 3: Chạy Agent
```bash
python main.py
```

---

## 🛠️ Cấu Trúc Dự Án
```text
daily_news_agent/
│
├── config.py             # Cấu hình nguồn tin RSS, API key, thư mục báo cáo
├── agent.py              # "Bộ não" của Agent: quy trình tư duy, lọc tin, gọi LLM/Offline
├── main.py               # File chính điều phối toàn bộ workflow
├── requirements.txt      # Thư viện phụ thuộc
├── .env.example          # Mẫu cấu hình API key
├── tools/                # Các "công cụ" Agent sử dụng
│   ├── news_fetcher.py   # Tool cào tin tức RSS từ mạng
│   └── notifier.py       # Tool tạo file Markdown, HTML Web và gửi Telegram
└── reports/              # Nơi lưu trữ các bản tin hàng ngày đã được tạo
```

---

## 💡 Tùy Biến
- Muốn thêm nguồn tin mới? Mở file `config.py` và thêm link RSS vào mảng `NEWS_SOURCES`.
- Muốn dùng AI Gemini để phân tích sâu: Tạo file `.env` từ `.env.example`, đổi `AI_PROVIDER=gemini` và dán API key của bạn vào.
