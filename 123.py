import os
import re
import subprocess
import time
import requests

# --- НАСТРОЙКИ ---
# ВСТАВЬ СВОЙ ТОКЕН НИЖЕ (в кавычках)
# Взять тут: https://dashboard.ngrok.com/get-started/your-authtoken
NGROK_TOKEN = "3BqjXitIFw8B84jFdkyYudSK8GV_5NoXRoJ52P1Lg2bbEs2jR" 

PORT = 8000
HTML_FILES = ["login.html", "register.html", "home.html", "store.html", "settings.html", "admin.html"]

def update_files(new_url):
    print(f"\n[!] Новая ссылка от Ngrok: {new_url}")
    # Ищем строку const API = "..." во всех файлах
    pattern = r'const\s+API\s*=\s*["\']https?://[^"\']+["\']\s*;?'
    replacement = f'const API = "{new_url}";'

    updated_count = 0
    for file_name in HTML_FILES:
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()
            
            if re.search(pattern, content):
                new_content = re.sub(pattern, replacement, content)
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"[+] ОБНОВЛЕНО: {file_name}")
                updated_count += 1
    
    if updated_count > 0:
        print("\n" + "="*50)
        print("ГОТОВО! Теперь сделай COMMIT и PUSH в GitHub Desktop.")
        print(f"Актуальная ссылка: {new_url}")
        print("="*50)

def start_ngrok():
    # Указываем точный путь к твоему ngrok.exe
    ngrok_path = r"C:\Users\Lenovo\Desktop\Titanium_Project\server\ngrok.exe"
    
    if not os.path.exists(ngrok_path):
        print(f"[!] ОШИБКА: Файл не найден по пути {ngrok_path}")
        return

    # Привязываем токен
    print("Авторизация Ngrok...")
    subprocess.run([ngrok_path, "config", "add-authtoken", NGROK_TOKEN])
    
    print("Запуск Ngrok туннеля...")
    # Запускаем Ngrok
    process = subprocess.Popen(
        [ngrok_path, "http", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    # Даем время на запуск
    time.sleep(4)
    
    try:
        # Получаем ссылку через локальный API Ngrok
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = response.json()
        public_url = data['tunnels'][0]['public_url']
        
        # GitHub Pages любит HTTPS
        if public_url.startswith("http://"):
            public_url = public_url.replace("http://", "https://")
            
        update_files(public_url)
    except Exception as e:
        print(f"\n[ОШИБКА] Не удалось достать ссылку. Убедись, что порт {PORT} свободен.")
        print(f"Детали: {e}")

    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nВыключение...")
        process.terminate()
    
    print("Запуск Ngrok туннеля...")
    # Запускаем Ngrok в фоновом режиме
    process = subprocess.Popen(
        ["ngrok", "http", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    # Даем время на запуск и получение ссылки
    time.sleep(3)
    
    try:
        # Ngrok имеет внутренний API на порту 4040, достаем ссылку оттуда
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = response.json()
        public_url = data['tunnels'][0]['public_url']
        
        # Если ссылка на http, меняем на https для GitHub
        if public_url.startswith("http://"):
            public_url = public_url.replace("http://", "https://")
            
        update_files(public_url)
    except Exception as e:
        print(f"\n[ОШИБКА] Не удалось получить ссылку: {e}")
        print("Проверь, что Ngrok установлен и запущен.")

    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nВыключение...")
        process.terminate()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== TITANIUM AUTO-TUNNEL (NGROK) ===")
    start_ngrok()