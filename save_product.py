import requests
import json
import os

# Tạo thư mục lưu ảnh nếu chưa có
image_folder = './product_images/phukienmacbook'
os.makedirs(image_folder, exist_ok=True)

# Đường dẫn tới file JSON duy nhất
json_file_path = 'phukienmacbook.json'

# Nếu file đã tồn tại, đọc nội dung hiện tại
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        all_products = json.load(json_file)
else:
    all_products = []

# Hàm để tải và lưu ảnh
def download_image(image_url, image_name):
    try:
        response = requests.get(image_url, stream=True)
            # Lưu ảnh vào thư mục chỉ định
        image_path = os.path.join(image_folder, image_name)
        with open(image_path, 'wb') as image_file:
            for chunk in response.iter_content(1024):
                image_file.write(chunk)
            print(f"Ảnh đã được lưu vào {image_path}")
            
    except Exception as e:
        print(f"Lỗi khi tải ảnh: {e}")

# Hàm để gọi API với id và lưu vào file JSON
def fetch_and_save_product():
    try:
        # Gọi API với id động
        url = f"https://ecomws.didongviet.vn/fe/v1/products?category_ids=440&orderBy=position&orderType=ASC&page=1&limit=1000"
        response = requests.get(url)
        
        # Kiểm tra nếu yêu cầu thành công (status code 200)
        if response.status_code == 200:
    
            json_data = response.json()
            product_data = json_data.get('data', {}).get('data', [])
            # Lấy đường dẫn ảnh từ JSON và tải ảnh
            for product in product_data:
                image_file = product.get('thumbnail', None)
                print("Đã lưu ảnh vào ", image_file)
                if image_file:
                    image_url = f"https://cdn-v2.didongviet.vn/{image_file}"
                    image_name = os.path.basename(image_file)
                    download_image(image_url, image_name)
            # Thêm sản phẩm vào danh sách chung
            all_products.append(product_data)
            print(f"Dữ liệu sản phẩm id {id} đã được thêm vào danh sách")

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
