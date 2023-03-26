document.getElementById('add-assignment-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    fetch('/add_assignment', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Append the new assignment to the table
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td>${data.assignment.id}</td>
                <td>${data.assignment.capacity}</td>
                <td>${data.assignment.member.name}</td>
                <td>${data.assignment.project.name}</td>
                <td>
                    <button type="button" class="btn btn-danger" onclick="deleteAssignment({{ assignment.id }})">Delete</button>
                </td>
            `;
            document.getElementById('assignments-tbody').appendChild(newRow);

            // Show the Toast
            const toastElement = document.getElementById('assignment-added-toast');
            const toast = new bootstrap.Toast(toastElement);
            toast.show();

            // Clear the form
            event.target.reset();
        } else {
            // Handle errors (e.g., display an error message)
            alert('Error adding assignment: ' + data.error);
        }
    });

});

document.getElementById('assignments-tbody').addEventListener('click', function (event) {
  if (event.target.classList.contains('btn-delete')) {
    deleteSkill(event);
  }
});

function deleteAssignment(assignmentId) {
  fetch('/delete_assignment/' + assignmentId, {
    method: 'DELETE',
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Remove the assignment row from the table
        const row = document.querySelector(`[data-assignment-id="${assignmentId}"]`);
        row.remove();
      } else {
        // Handle errors (e.g., display an error message)
        alert('Error deleting assignment: ' + data.error);
      }
    });
}
