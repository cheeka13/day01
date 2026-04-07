# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature tăng dần, câu trả lời chuyển từ trạng thái khách quan và lặp lại sang trạng thái phong phú về từ vựng và đa dạng chủ đề hơn. Tuy nhiên, khi đạt đến mức 1.5, câu trả lời thêm cả về chủ đề khác (cà phê) và sử dụng từ ngữ mô tả mạnh hơn, do mô hình ưu tiên các từ ngữ có xác suất thấp để tạo sự đột phá.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Tôi sẽ đặt ở mức dưới 0.5 để mang lại sự ổn định và khách quan cho câu trả lời và giảm thiểu sự hallucination. Khách hàng cần thông tin đúng và chuẩn xác.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Tính toán: 
- Tổng token output mỗi ngày: 10.000 users × 3 calls × 350 tokens = 10.5 triệu tokens
- Chi phí GPT-4o: (10.5M / 1000) × $0.010 = $105/ngày
- Chi phí GPT-4o-mini: (10.5M / 1000) × $0.0006 = $6.30/ngày
- Tỷ lệ: $105 / $6.30 ≈ 16.67 lần. GPT-4o đắt hơn GPT-4o-mini khoảng 17 lần.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> Trường hợp chọn GPT-4o: Debug memory leak trong ứng dụng React Native mà tôi đang phát triển. GPT-4o sẽ nhìn ra sự tương quan giữa các component tốt hơn với khả năng reasoning và lập luận logic tốt hơn.
Trường hợp chọn GPT-4o-mini: Tóm tắt nội dung các bài báo muốn đọc hàng ngày, do không cần tốc độ cao, độ chính xác vừa phải và giá thành thấp.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming là lựa chọn bắt buộc khi thời gian phản hồi tổng thể quá dài, khiến người dùng có cảm giác ứng dụng bị treo. Trong khi đó, Non-streaming phù hợp cho các tác vụ "hậu trường", nơi mà sự chính xác và khả năng xử lý dữ liệu quan trọng hơn việc hiển thị tức thì.
Streaming cần thiết khi dùng cho các chat bot giao tiếp trực tiếp, viết nội dung dài hay cần giảm tỉ lệ drop off. Non-streaming phù hợp với xử lý dữ liệu hay các tác vụ cần validation, hoặc tích hợp API


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
