from langchain_core.tools import tool

# ==========================================
# MOCK DATA - Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Đây là dữ liệu (VD: cuối tuần đặt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu trước khi dùng toolasses.
# ==========================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:30", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "08:15", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_900_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "10:00", "price": 2_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:30", "price": 850_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_200_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_500_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_100_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:05", "price": 850_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 8.5},
        {"name": "Sala Đà Nẵng Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 8.2},
        {"name": "Titvicel Beach Hotel", "stars": 3, "price_per_night": 450_000, "area": "Sơn Trà", "rating": 6.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 200_000, "area": "Mỹ Khê", "rating": 7.0},
        {"name": "An Thượng", "stars": 1, "price_per_night": 350_000, "area": "An Thượng", "rating": 6.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Dương Đông", "rating": 8.1},
        {"name": "Bãi Trường", "stars": 3, "price_per_night": 800_000, "area": "Bãi Trường", "rating": 8.0},
        {"name": "Dương Đông", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 6.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 8.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 8.1},
        {"name": "Quận 3", "stars": 3, "price_per_night": 500_000, "area": "Quận 3", "rating": 7.5},
        {"name": "The Common", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 6.4},
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.

    Tham số:
        - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
        - destination: thành phố đích (VD: 'Đà Nẵng', 'Phú Quốc')

    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    flights = FLIGHTS_DB.get((origin, destination))
    
    if not flights:
        # Kiểm tra chiều ngược lại
        reverse_flights = FLIGHTS_DB.get((destination, origin))
        if reverse_flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}. Tuy nhiên, chúng mình có chuyến ngược lại từ {destination} về {origin}, bạn có muốn xem không?"
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    result = f"Tìm thấy {len(flights)} chuyến bay từ {origin} đến {destination}:\n"
    for flight in flights:
        # Format giá tiền: 1.450.000đ
        price_formatted = f"{flight['price']:,}".replace(",", ".") + "đ"
        result += f"- {flight['airline']}: {flight['departure']} -> {flight['arrival']} ({flight['class']}) - Giá: {price_formatted}\n"
    
    return result.strip()


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Tham số:
        - city: tên thành phố (VD: 'Đà Nẵng', 'Hồ Chí Minh')
        - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn
        - rating: đánh giá sao
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating
    """
    hotels = HOTELS_DB.get(city, [])
    
    # Lọc theo giá
    filtered_hotels = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
    
    if not filtered_hotels:
        if not hotels:
            return f"Xin lỗi, hiện tại mình chưa có thông tin khách sạn tại {city}."
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {max_price_per_night:,}.000đ/đêm. Bạn thử tăng ngân sách một chút xem sao nhé!"

    # Sắp xếp theo rating giảm dần
    sorted_hotels = sorted(filtered_hotels, key=lambda x: x['rating'], reverse=True)

    result = f"Tìm thấy {len(sorted_hotels)} khách sạn tại {city} phù hợp với yêu cầu của bạn:\n"
    for hotel in sorted_hotels:
        price_formatted = f"{hotel['price_per_night']:,}".replace(",", ".") + "đ"
        result += f"- {hotel['name']} ({hotel['stars']} sao): {price_formatted}/đêm | Khu vực: {hotel['area']} | Đánh giá: {hotel['rating']}/10\n"
    
    return result.strip()


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Tham số:
        - total_budget: tổng ngân sách ban đầu (VND)
        - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy, định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bản chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu
    """
    try:
        # Parse chuỗi expenses thành dict {tên: số_tiền}
        # Ví dụ: 'vé_máy_bay:890000,khách_sạn:650000'
        expense_list = expenses.split(',')
        parsed_expenses = {}
        total_costs = 0
        
        detail_lines = []
        for item in expense_list:
            if not item.strip(): continue
            name, price_str = item.split(':')
            name = name.strip().replace('_', ' ').capitalize()
            price = int(price_str.strip())
            parsed_expenses[name] = price
            total_costs += price
            detail_lines.append(f"- {name}: {price:,}".replace(",", ".") + "đ")

        balance = total_budget - total_costs
        
        result = "=== Bảng Chi Phí Dự Kiến ===\n"
        result += "\n".join(detail_lines) + "\n"
        result += "---------------------------\n"
        result += f"Tổng chi: {total_costs:,}".replace(",", ".") + "đ\n"
        result += f"Ngân sách: {total_budget:,}".replace(",", ".") + "đ\n"
        
        if balance >= 0:
            result += f"Còn lại: {balance:,}".replace(",", ".") + "đ\n"
            result += "=> Bạn vẫn còn dư ngân sách, quẩy thôi!"
        else:
            result += f"CẢNH BÁO: Bạn đang vượt ngân sách {abs(balance):,}".replace(",", ".") + "đ!\n"
            result += "=> Hãy cân nhắc chọn vé máy bay hoặc khách sạn giá rẻ hơn nhé."
            
        return result
        
    except (ValueError, IndexError):
        return "Lỗi: Định dạng chuỗi chi phí (expenses) không đúng. Vui lòng dùng định dạng 'khoản_chi:số_tiền,khoản_chi:số_tiền'."


# Chú ý:
# - search_flights: phải xử lý tuple key, thử tra ngược chiều
# - search_hotels: phải lọc + sắp xếp, không chỉ lookup
# - calculate_budget: phải parse chuỗi, xử lý format lỗi, tính toán thực sự
# 3 tools có MỐI LIÊN HỆ: kết quả flights -> input cho budget -> quyết định hotels
