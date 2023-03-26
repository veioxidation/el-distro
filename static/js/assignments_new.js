function handleItemForm(event, action, endpoint) {
  event.preventDefault();

  const formData = new FormData(event.target);
  fetch(endpoint, {
    method: action,
    body: formData,
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Append the new item to the table
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td>${data.item.id}</td>
        <td>${data.item.name}</td>
        <td>${data.item.capacity || '-'}</td>
        <td>${data.item.start_date || '-'}</td>
        <td>${data.item.end_date || '-'}</td>
        <td>
          <button class="btn btn-primary btn-sm edit-item" data-item-id="${data.item.id}">Edit</button>
          <button class="btn btn-danger btn-sm delete-item" data-item-id="${data.item.id}">Delete</button>
        </td>
      `;
      document.getElementById('items-tbody').appendChild(newRow);

      // Clear the form
      event.target.reset();

      // Show success message
      showMessage('Item has been added successfully.', 'alert-success');
    } else {
      // Handle errors (e.g., display an error message)
      showMessage('Error adding item: ' + data.error, 'alert-danger');
    }
  });
}



function createAssignmentRow(data) {
  const newRow = document.createElement('tr');
  newRow.dataset.itemId = data.assignment.id;
  newRow.innerHTML = `
    <td>${data.assignment.id}</td>
    <td>${data.assignment.member.name}</td>
    <td>${data.assignment.project.name}</td>
    <td>${data.assignment.capacity}</td>
    <td>
      <button type="button" class="btn btn-danger btn-delete" data-item-id="${data.assignment.id}">Delete</button>
    </td>
  `;
  return newRow;
}



// Handle assignment form submit
document.getElementById('assignment-form').addEventListener('submit', function(event) {
  const assignmentId = document.getElementById('assignment-id').value;
  const action = assignmentId ? 'PUT' : 'POST';
  const endpoint = assignmentId ? `/assignments/${assignmentId}` : '/assignments';

  handleItemForm(event, action, endpoint);
});

// Handle edit item click
document.addEventListener('click', function(event) {
  if (event.target.classList.contains('edit-item')) {
    const itemId = event.target.dataset.itemId;
    fetch(`/assignments/${itemId}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Set form fields with item data
        document.getElementById('assignment-id').value = data.assignment.id;
        document.getElementById('member-select').value = data.assignment.member_id;
        document.getElementById('project-select').value = data.assignment.project_id;
        document.getElementById('capacity').value = data.assignment.capacity;
      } else {
        // Handle errors (e.g., display an error message)
        showMessage('Error loading assignment data: ' + data.error, 'alert-danger');
      }
    });
  }
});

// Handle delete item click
document.addEventListener('click', function(event) {
  if (event.target.classList.contains('delete-item')) {
    const itemId = event.target.dataset.itemId;
    if (confirm('Are you sure you want to delete this assignment?')) {
      fetch(`/assignments/${itemId}`, {
        method: 'DELETE'
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Remove the deleted item from the table
          const row = event.target.closest('tr');
          row.parentNode.removeChild(row);

          // Show success message
          showMessage('Assignment has been deleted successfully.', 'alert-success');
        } else {
          // Handle errors (e.g., display an error message)
          showMessage('Error deleting assignment: ' + data.error, 'alert-danger');
        }
      });
    }
  }
});
