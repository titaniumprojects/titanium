const API = "https://heptarchal-stanton-hemispheric.ngrok-free.dev";

// Функция для получения данных пользователя
async function fetchUserData(username) {
    try {
        const res = await fetch(`${API}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username, password: "" }) // В твоем server.py пустой пароль разрешен для получения данных
        });
        return await res.json();
    } catch (e) {
        console.error("Ошибка связи с сервером");
        return null;
    }
}