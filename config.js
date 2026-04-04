// Конфигурация API
const API = "https://heptarchal-stanton-hemispheric.ngrok-free.dev";

// Проверка авторизации (утилита)
function checkAuth() {
    const user = localStorage.getItem('username');
    if (!user && !window.location.pathname.includes('login.html') && !window.location.pathname.includes('register.html')) {
        window.location.href = "login.html";
    }
    return user;
}