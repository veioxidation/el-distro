document.getElementById('add-project-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  fetch('/add_project', {
    method: 'POST',
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Append the new project to the table
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
          <td>${data.project.id}</td>
          <td>${data.project.name}</td>
          <td>${data.project.effort_estimate}</td>
          <td>${data.project.start_date}</td>
          <td>${data.project.due_date}</td>
          <td>
            <button type="button" class="btn btn-danger" onclick="deleteProject({{ project.id }})">Delete</button>
          </td>
        `;
        document.getElementById('projects-tbody').appendChild(newRow);

        // Clear the form
        event.target.reset();

        // Show the Toast
        const toastElement = document.getElementById('project-added-toast');
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
      } else {
        // Handle errors (e.g., display an error message)
        alert('Error adding project: ' + data.error);
      }
    });
});

document.getElementById('projects-tbody').addEventListener('click', function (event) {
  if (event.target.classList.contains('btn-delete')) {
    deleteProject(event);
  }
});



function deleteProject(projectId) {
  fetch('/delete_project/' + projectId, {
    method: 'DELETE',
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Remove the member row from the table
        const row = document.querySelector(`[data-project-id="${projectId}"]`);
        row.remove();
      } else {
        // Handle errors (e.g., display an error message)
        alert('Error deleting project: ' + data.error);
      }
    });
}
