import json

# Đọc dữ liệu từ file JSON
file_path = './Main/iphone.json'
prefix_folder = 'iphone/'
output_path_root = './Main_1/iphone.json'

# Hàm chuyển đổi dữ liệu từ JSON thành các thuộc tính cần thiết
def transform_product_data(data):
    transformed_data = []

    # Xác định các trường cần lấy và tên mới cho children_products
    required_fields = {
        'product_id': 'product_sub_id',
        'product': 'product_name',
        'product_code': 'barcode',
        'thumbnail': 'thumbnail',
        'slug': 'product_slug',
        'price': 'product_price',
        'short_description' : 'short_description',
        'promo_text' : 'description',
        'root_category_slug' : 'categorySlug',
        'meta_image' : 'product_images'
    }

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):  # Kiểm tra xem item có phải là dictionary không
                # Lấy các trường cần thiết từ sản phẩm chính
                transformed_item = {
                    'product_id': item.get('product_id'),
                    'product_name': item.get('product'),
                    'thumbnail': item.get('thumbnail'),
                    'barcode': item.get('product_code'),
                    'product_images': item.get('images'),
                    'product_slug': item.get('slug'),
                    'product_price': item.get('price'),
                    'promotion_note': item.get('promotion_note'),
                    'short_description' : item.get('short_description'),
                    'description' : item.get('promo_text'),
                    'url_video' : item.get('url_media'),
                    'categorySlug' : item.get('categorySlug')
                }
                
                # Xử lý thumbnail để chỉ lấy tên file và thêm tiền tố
                if 'thumbnail' in item:
                    transformed_item['thumbnail'] = prefix_folder + item['thumbnail'].split('/')[-1]
                
                # Xử lý product_images để chỉ lấy tên file và thêm tiền tố
                if 'images' in item:
                    transformed_item['product_images'] = [
                        prefix_folder + img.split('/')[-1] for img in item['images']
                    ]    

                # Kiểm tra và xử lý trường productSubs (children_products)
                if 'children_products' in item:
                    # Lọc các trường cần thiết trong từng sản phẩm con và đặt tên trường mới
                    product_subs = []
                    for child in item['children_products']:
                        filtered_child = {
                            new_key: child.get(old_key)
                            for old_key, new_key in required_fields.items()
                            if old_key in child
                        }

                        # Xử lý thumbnail trong children_products và thêm tiền tố
                        if 'thumbnail' in child:
                            filtered_child['thumbnail'] = prefix_folder + child['thumbnail'].split('/')[-1]

                        # Xử lý meta_image trong children_products nếu là chuỗi
                        if 'meta_image' in child:
                            meta_image = child.get('meta_image')
                            if isinstance(meta_image, str):  # Kiểm tra meta_image có phải là chuỗi không
                                filtered_child['product_images'] = prefix_folder + meta_image.split('/')[-1]
                            else:
                                print(f"Cảnh báo: Trường meta_image không phải là chuỗi trong product con {child.get('product_id')}")

                        product_subs.append(filtered_child)
                    
                    # Thêm productSubs vào transformed_item
                    transformed_item['productSubs'] = product_subs

                # Thêm sản phẩm đã xử lý vào danh sách kết quả
                transformed_data.append(transformed_item)
            else:
                print("Cảnh báo: Dữ liệu không hợp lệ (item không phải là dictionary).")
    else:
        print("Cảnh báo: Dữ liệu không phải là một danh sách.")

    return transformed_data

# Đọc file JSON và xử lý dữ liệu
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        # Chuyển đổi dữ liệu thành các thuộc tính cần thiết
        transformed_data = transform_product_data(data)

        # (Tùy chọn) Lưu kết quả vào file mới
        output_path = output_path_root
        with open(output_path, 'w', encoding='utf-8') as output_file:
            json.dump(transformed_data, output_file, indent=2, ensure_ascii=False)

        print(f'Dữ liệu đã được lưu vào {output_path}')
except FileNotFoundError:
    print(f"Không tìm thấy file tại: {file_path}")
except json.JSONDecodeError:
    print("File JSON không hợp lệ hoặc có lỗi cú pháp.")
