function changeTextColorAndRedirect(button, url) {
  button.style.color = 'orange';

  // Redirect to the URL
  setTimeout(function() {
    location.href = url;
  }, 100); 
}

document.addEventListener('DOMContentLoaded', function() {
  fetchStudentInfo();
  highlightAbsences();
});

async function fetchStudentInfo() {
  try {
      // Предполагается, что URL указывает на место, где хранится ваш JSON
      const response = await fetch('path_to_your_student_info.json');
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      const studentData = await response.json();
      updateStudentInfo(studentData);
  } catch (error) {
      console.error('Ошибка при получении данных о студенте:', error);
  }
}

function updateStudentInfo(data) {
  // Обновляем информацию о студенте
  document.getElementById('studentName').textContent = data.nameSurname;
  document.getElementById('id').textContent = data.id;
  document.getElementById('advisorName').textContent = data.advisor;
  document.getElementById('majorProgram').textContent = data.majorProgram;

  // Обновляем таблицу предметов
  updateCoursesTable(data.courses);
}

function updateCoursesTable(courses) {
  const tableBody = document.querySelector('table tbody');
  tableBody.innerHTML = ''; // Очищаем текущие строки таблицы

  courses.forEach(course => {
      const row = document.createElement('tr');
      row.innerHTML = `
          <td><a href="${course.link}" class="course-link">${course.code}</a></td>
          <td><a href="${course.link}" class="course-link">${course.name}</a></td>
          <td>${course.credits}</td>
          <td>${course.ects}</td>
          <td>${course.hours}</td>
          <td>${course.passed}</td>
          <td>${course.failed}</td>
          <td>${course.pending}</td>
          <td>${course.absencePercentage}%</td>
      `;
      if (course.absencePercentage >= 30) {
          row.style.backgroundColor = '#ffcccc'; // Выделение красным цветом
      }
      tableBody.appendChild(row);
  });
}