// Твой статический URL ngrok
const API = "https://heptarchal-stanton-hemispheric.ngrok-free.dev";

// Добавляем глобальную настройку для fetch, чтобы ngrok не показывал страницу-заглушку
const originalFetch = window.fetch;
window.fetch = function() {
    let [resource, config] = arguments;
    if (!config) config = {};
    if (!config.headers) config.headers = {};
    
    // Добавляем заголовок, который отключает предупреждение ngrok
    config.headers['ngrok-skip-browser-warning'] = 'true';
    
    return originalFetch(resource, config);
};