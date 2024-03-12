function goBack() {
    window.history.back(); // Встроенная функция JavaScript для возврата на предыдущую страницу в истории браузера
}
// Получаем ссылки на элементы с помощью их идентификаторов
const courseLinks = document.querySelectorAll('.course-link');

// Обработчик нажатия на предмет
function handleCourseClick(event) {
    // Отменяем стандартное действие ссылки (переход по ссылке)
    event.preventDefault();
    
    // Получаем ссылку на предмет
    const courseLink = event.target.getAttribute('href');
    
    // Перенаправляем пользователя на страницу с предметом
    window.location.href = courseLink;
}

// Добавляем обработчик нажатия для каждой ссылки на предмет
courseLinks.forEach(link => {
    link.addEventListener('click', handleCourseClick);
});

