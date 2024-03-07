function setupEventListeners() {
  // For editing
  const editButtons = document.querySelectorAll('.editButton');
  editButtons.forEach(button => {
    button.addEventListener('click', function () {
      const targetFormId = this.getAttribute('data-target-form');
      const targetForm = document.getElementById(targetFormId);
      if (targetForm.style.display === 'none' || targetForm.style.display === '') {
        targetForm.style.display = 'block';
      }
    });
  });

  // For trading
  document.querySelectorAll('.tradeButton').forEach(button => {
    button.addEventListener('click', function () {
      const itemId = this.getAttribute('data-item-id');
      const itemImages = document.querySelectorAll(`.item-${itemId}`);
      itemImages.forEach(image => {
        if (image.classList.contains('darkened')) {
          image.classList.remove('darkened');
        } else {
          image.classList.add('darkened');
        }
      });

      fetch(`/toggle_trade/${itemId}`, {method: 'POST'})
        .then(response => {
          if (response.ok) {
            location.reload();
          } else {
            console.error('Failed to update trade status');
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  });
}

document.addEventListener('DOMContentLoaded', setupEventListeners);
window.onload = setupEventListeners;
