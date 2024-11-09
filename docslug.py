import json
import requests
import os

# Hàm trích xuất và in giá trị của "slug" cho từng sản phẩm
def extract_slugs(file_path):
    # Đọc dữ liệu từ file JSON
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Tạo danh sách chứa slug
    slugs = []
    for product_list in data:
        for product in product_list:
            slug_value = product.get("slug")
            if slug_value:
                slugs.append(slug_value)
    
    return slugs 

# Đường dẫn tới file JSON đầu vào và đầu ra
input_json_file_path = './Xiaomi.json'  # Thay đổi đường dẫn nếu cần
output_json_file_path = './Main/xiaomi.json'  # Thay đổi đường dẫn nếu cần

# Tạo thư mục đầu ra nếu chưa có
output_folder = os.path.dirname(output_json_file_path)
os.makedirs(output_folder, exist_ok=True)

# Nếu file đầu vào đã tồn tại, đọc nội dung hiện tại
if os.path.exists(input_json_file_path):
    with open(input_json_file_path, 'r', encoding='utf-8') as json_file:
        all_products = json.load(json_file)
else:
    print(f"File đầu vào {input_json_file_path} không tồn tại.")
    all_products = []

# Hàm để gọi API với slug và lưu vào file JSON
def fetch_and_save_product():
    try:
        slugs = extract_slugs(input_json_file_path)  # Trích xuất slug từ file đầu vào
        
        for slug in slugs:
            # Gọi API với slug
            url = f"https://ecomws.didongviet.vn/fe/v1/products/{slug}"
            response = requests.get(url)
            
            # Kiểm tra nếu yêu cầu thành công (status code 200)
            if response.status_code == 200:
                json_data = response.json()
                product_data = json_data.get('data', {})
                all_products.append(product_data)
                print(f"Dữ liệu sản phẩm với slug '{slug}' đã được thêm vào danh sách.")
            else:
                print(f"Lỗi khi gọi API với slug '{slug}': {response.status_code}")
    except Exception as e:
        print(f"Lỗi khi gọi API hoặc lưu dữ liệu: {e}")

# Gọi hàm để lấy dữ liệu sản phẩm
fetch_and_save_product()

# Sau khi lấy xong tất cả sản phẩm, lưu vào file JSON đầu ra
with open(output_json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_products, json_file, ensure_ascii=False, indent=2)

print(f"Tất cả dữ liệu sản phẩm đã được lưu vào {output_json_file_path}")
