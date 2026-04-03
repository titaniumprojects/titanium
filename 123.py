import os
import re
import subprocess
import time

# --- НАСТРОЙКИ ---
PORT = 8000
# Список всех файлов, где нужно менять ссылку
HTML_FILES = ["login.html", "register.html", "home.html", "store.html", "settings.html", "admin.html"]

def update_files(new_url):
    print(f"\n[!] Новая ссылка от Serveo: {new_url}")
    
    # Регулярное выражение: ищет const API = "любой_адрес";
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
            else:
                print(f"[-] Пропуск: {file_name} (строка const API не найдена)")
    
    if updated_count > 0:
        print("\n" + "="*50)
        print("УСПЕХ! Ссылки обновлены локально.")
        print("Теперь зайди в GitHub Desktop и сделай PUSH.")
        print(f"Твой API теперь тут: {new_url}")
        print("="*50)

def start_serveo():
    # Пытаемся найти путь к ssh в системе
    ssh_path = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', 'OpenSSH', 'ssh.exe')
    if not os.path.exists(ssh_path):
        ssh_path = "ssh" # Если по точному пути нет, надеемся на переменную PATH

    print(f"Запуск туннеля через {ssh_path}...")
    
    # Команда запуска туннеля
    # -o StrictHostKeyChecking=no чтобы не спрашивал подтверждение (по возможности)
    # -R 80:localhost:8000 перенаправляет порт 8000 на сервер serveo.net
    process = subprocess.Popen(
        [ssh_path, "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8000", "serveo.net"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        bufsize=1
    )

    url_found = False
    try:
        for line in process.stdout:
            line = line.strip()
            print(f"> {line}") # Видим всё, что пишет сервер

            # Ищем заветную ссылку https://....serveo.net
            match = re.search(r"https://[a-zA-Z0-9.-]+\.serveo\.net", line)
            if match and not url_found:
                url = match.group(0)
                update_files(url)
                url_found = True
                print("\n[ИНФО] Туннель активен. Не закрывай это окно!")
            
            # Если SSH попросит ручное подтверждение (иногда бывает)
            if "Are you sure you want to continue" in line:
                print("\n[!!!] ВНИМАНИЕ: Введи 'yes' прямо в этой консоли и нажми Enter!")

        process.wait()
    except KeyboardInterrupt:
        print("\n[!] Выключение туннеля...")
        process.terminate()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== TITANIUM AUTO-TUNNEL (SERVEO) ===")
    start_serveo()