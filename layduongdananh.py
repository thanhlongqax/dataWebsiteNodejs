import json
import requests
import os

def find_all_image_paths(data, image_paths=None):
    if image_paths is None:
        image_paths = []

    # Nếu dữ liệu là dictionary, duyệt qua từng cặp key-value
    if isinstance(data, dict):
        for key, value in data.items():
            # Kiểm tra nếu value là chuỗi và có đường dẫn bắt đầu bằng "files/media"
            if isinstance(value, str) and value.startswith("files"):
                image_paths.append(value)  # Thêm đường dẫn vào danh sách
            # Đệ quy nếu value là dictionary hoặc list
            find_all_image_paths(value, image_paths)
    
    # Nếu dữ liệu là một list, duyệt qua từng phần tử
    elif isinstance(data, list):
        for item in data:
            find_all_image_paths(item, image_paths)
    
    return image_paths

# Hàm đọc file JSON và tìm tất cả đường dẫn ảnh
def extract_all_images(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    image_paths = find_all_image_paths(data)
    return image_paths

# Hàm để tải và lưu ảnh
def download_image(image_url, image_folder):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        
        # Lấy tên ảnh từ URL (có thể thay đổi nếu cần)
        image_name = image_url.split("/")[-1]
        image_path = os.path.join(image_folder, image_name)

        # Lưu ảnh vào thư mục chỉ định
        with open(image_path, 'wb') as image_file:
            for chunk in response.iter_content(1024):
                image_file.write(chunk)

        print(f"Ảnh đã được lưu vào {image_path}")
        
    except Exception as e:
        print(f"Lỗi khi tải ảnh: {e}")

# Đường dẫn tới file JSON của bạn
file_path = "./Main/xiaomi.json"  
# Đường dẫn tới thư mục lưu ảnh
image_folder = './Main/product_image/xiaomi'
os.makedirs(image_folder, exist_ok=True)  # Tạo thư mục nếu chưa có

# Gọi hàm để lấy tất cả đường dẫn ảnh
all_images = extract_all_images(file_path)

print("Danh sách tất cả đường dẫn ảnh:", all_images)
image_url = "https://cdn-v2.didongviet.vn/{}"
# Tải ảnh từ tất cả đường dẫn đã tìm được
for image_path in all_images:
    print(image_path)
    download_image(f"https://cdn-v2.didongviet.vn/{image_path}", image_folder)