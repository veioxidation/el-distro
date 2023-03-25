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
                <td>${data.member.name}</td>
                <td>${data.member.skills.join(', ')}</td>
                <td>${data.member.capacity}</td>
            `;
            document.getElementById('members-tbody').appendChild(newRow);

            // Clear the form
            event.target.reset();
        } else {
            // Handle errors (e.g., display an error message)
            alert('Error adding member: ' + data.error);
        }
    });
});
