# main.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",  # Cho phép truy cập từ mọi IP
        port=8080,       # Port
        debug=True       # (dev mode)
    )