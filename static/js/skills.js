document.getElementById('add-skill-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  fetch('/add_skill', {
    method: 'POST',
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Append the new skill to the table
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
          <td>${data.skill.id}</td>
          <td>${data.skill.name}</td>
          <td>
            <button type="button" class="btn btn-danger" onclick="deleteSkill({{ skill.id }})">Delete</button>
          </td>
        `;
        document.getElementById('skills-tbody').appendChild(newRow);

        // Clear the form
        event.target.reset();

        // Show the Toast
        const toastElement = document.getElementById('skill-added-toast');
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
      } else {
        // Handle errors (e.g., display an error message)
        alert('Error adding skill: ' + data.error);
      }
    });
});

document.getElementById('skills-tbody').addEventListener('click', function (event) {
  if (event.target.classList.contains('btn-delete')) {
    deleteSkill(event);
  }
});


function deleteSkill(skillId) {
  fetch('/delete_skill/' + skillId, {
    method: 'DELETE',
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Remove the member row from the table
        const row = document.querySelector(`[data-skill-id="${skillId}"]`);
        row.remove();
      } else {
        // Handle errors (e.g., display an error message)
        alert('Error deleting skill: ' + data.error);
      }
    });
}
