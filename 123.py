import os
import re
import subprocess

# --- НАСТРОЙКИ ---
PORT = 8000
HTML_FILES = ["login.html", "register.html", "home.html", "store.html", "settings.html", "admin.html"]
LT_PATH = r"C:\node.js\lt.cmd"

def update_files(new_url):
    print(f"\n[!] Новая цель: {new_url}")
    
    # УЛЬТРА-ПОИСК: Ищет const API = "ЧТО УГОДНО"; 
    # Заменит и ngrok, и старые loca.lt, и любые другие ссылки
    pattern = r'const\s+API\s*=\s*["\']https?://[^"\']+["\']\s*;?'
    replacement = f'const API = "{new_url}";'

    updated_count = 0
    for file_name in HTML_FILES:
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if re.search(pattern, content):
                new_content = re.sub(pattern, replacement, content)
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"[+] ОБНОВЛЕНО: {file_name}")
                updated_count += 1
            else:
                # Если всё равно не нашел, значит в файле ошибка в названии переменной
                print(f"[-] ОШИБКА: В {file_name} не найдена переменная 'const API'")
        else:
            print(f"[?] Пропуск: {file_name} (файл не найден)")
    
    if updated_count > 0:
        print("\n" + "="*50)
        print("ПОБЕДА! Теперь точно все файлы обновлены.")
        print("Жми Commit/Push в GitHub Desktop!")
        print("="*50)

def start_tunnel():
    if not os.path.exists(LT_PATH):
        print(f"ОШИБКА: Не найден {LT_PATH}")
        return

    print("Запуск туннеля...")
    process = subprocess.Popen([LT_PATH, "--port", str(PORT)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
    
    try:
        for line in process.stdout:
            line = line.strip()
            print(f"> {line}")
            if "your url is:" in line:
                url = line.split("is:")[1].strip()
                update_files(url)
        process.wait()
    except KeyboardInterrupt:
        process.terminate()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    start_tunnel()