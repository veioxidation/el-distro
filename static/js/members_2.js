function handleItemForm(formId, tableBodyId, submitUrl, createRowCallback) {
  const form = document.getElementById(formId);
  const tableBody = document.getElementById(tableBodyId);

  form.addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    fetch(submitUrl, {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Create a new row using the provided callback function
          const newRow = createRowCallback(data);
          tableBody.appendChild(newRow);
          event.target.reset();
        } else {
          alert(`Error: ${data.error}`);
        }
      });
  });

  // Delegate click event to delete buttons
  tableBody.addEventListener('click', function (event) {
    if (event.target.classList.contains('btn-delete')) {
      event.preventDefault();
      const itemId = event.target.dataset.itemId;

      fetch(submitUrl + itemId, {
        method: 'DELETE',
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            const row = document.querySelector(`[data-item-id="${itemId}"]`);
            row.remove();
          } else {
            alert(`Error: ${data.error}`);
          }
        });
    }
  });
}
``


