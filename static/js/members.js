document.getElementById('add-member-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    fetch('/add_member', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Append the new member to the table
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td>${data.member.id}</td>
                <td>${data.member.name}</td>
                <td>${data.member.capacity}</td>
                <td>` + data.member.skills_list.join(', ') + `</td>
                <td></td>
            `;
            document.getElementById('members-tbody').appendChild(newRow);

            // Show the Toast
            const toastElement = document.getElementById('member-added-toast');
            const toast = new bootstrap.Toast(toastElement);
            toast.show();

            // Clear the form
            event.target.reset();
        } else {
            // Handle errors (e.g., display an error message)
            alert('Error adding member: ' + data.error);
        }
    });

});

document.getElementById('members-tbody').addEventListener('click', function (event) {
  if (event.target.classList.contains('btn-delete')) {
    deleteSkill(event);
  }
});

function deleteMember(memberId) {
  fetch('/delete_member/' + memberId, {
    method: 'DELETE',
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Remove the member row from the table
        const row = document.querySelector(`[data-member-id="${memberId}"]`);
        row.remove();
      } else {
        // Handle errors (e.g., display an error message)
        alert('Error deleting member: ' + data.error);
      }
    });
}
