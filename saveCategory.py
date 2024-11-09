import requests
import json
import os

# Đường dẫn tới file JSON duy nhất
json_file_path = 'all_products.json'

# Nếu file đã tồn tại, đọc nội dung hiện tại
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        all_products = json.load(json_file)
else:
    all_products = []


# Hàm để gọi API với id và lưu vào file JSON
def fetch_and_save_product():
    try:
        # Gọi API với id động
        url = f"https://ecomws.didongviet.vn/fe/v1/category"
        response = requests.get(url)
        
        # Kiểm tra nếu yêu cầu thành công (status code 200)
        if response.status_code == 200:
             
            json_data = response.json()
            product_data = json_data.get('data', {})
            # Thêm sản phẩm vào danh sách chung
            all_products.append(product_data)

        else:
            print(f"Lỗi khi gọi API với id {id}: {response.status_code}")
    except Exception as e:
        print(f"Lỗi khi gọi API hoặc lưu dữ liệu: {e}")

# Chạy hàm với id từ 1 đến 10 (có thể thay đổi)
# start_id = 501
# max_id = 1000

fetch_and_save_product()

# Sau khi lấy xong tất cả sản phẩm, lưu vào file JSON duy nhất
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_products, json_file, ensure_ascii=False, indent=2)

print(f"Tất cả dữ liệu sản phẩm đã được lưu vào {json_file_path}")
