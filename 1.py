import re
import json
import urllib.request
from pathlib import Path

def get_ngrok_url():
    """Получает публичный HTTPS URL из локального API ngrok"""
    try:
        with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels") as response:
            data = json.loads(response.read().decode())
            for tunnel in data["tunnels"]:
                if tunnel["proto"] == "https":
                    return tunnel["public_url"]
    except Exception as e:
        print(f"⚠️ Не удалось получить ngrok URL: {e}")
    print("⚠️ Использую localhost:8000 (для локального теста)")
    return "http://localhost:8000"

def update_html_files(directory="."):
    ngrok_url = get_ngrok_url()
    print(f"🔗 Использую URL: {ngrok_url}")

    for html_file in Path(directory).glob("*.html"):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Удаляем строку с подключением config.js
        content = re.sub(r'<script src="config\.js"></script>\s*\n?', '', content)

        # 2. Заменяем плейсхолдер PLACEHOLDER на реальный URL
        content = re.sub(r'const API = "PLACEHOLDER";', f'const API = "{ngrok_url}";', content)

        # 3. На случай, если в файле уже была старая ссылка — тоже заменяем
        content = re.sub(r'const API = "https?://[^"]+";', f'const API = "{ngrok_url}";', content)

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Обновлён: {html_file.name}")

if __name__ == "__main__":
    update_html_files()