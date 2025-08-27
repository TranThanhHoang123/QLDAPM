import os
from werkzeug.utils import secure_filename


def save_image(file, directory="events"):
    """
    Lưu file ảnh vào app/static/images/<directory>.

    Args:
        file: File từ request.files (werkzeug FileStorage)
        directory (str): Tên thư mục con để lưu (vd: 'events')

    Returns:
        str: Đường dẫn tương đối của file đã lưu (ví dụ: 'images/events/file.png')
    """
    if not file:
        return None

    # Gốc lưu trữ
    base_dir = os.path.join("app", "static", "images", directory)
    os.makedirs(base_dir, exist_ok=True)

    # Xử lý tên file an toàn
    filename = secure_filename(file.filename)
    filepath = os.path.join(base_dir, filename)

    # Nếu file trùng thì thêm số phía sau
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filepath):
        filename = f"{base}_{counter}{ext}"
        filepath = os.path.join(base_dir, filename)
        counter += 1

    # Lưu file
    file.save(filepath)

    # Trả về đường dẫn để lưu trong DB (dùng cho url_for('static', filename=...))
    return f"images/{directory}/{filename}"
