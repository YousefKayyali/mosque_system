console.log("student_review.js loaded");
document.addEventListener('DOMContentLoaded', function() {
  const mySelect = document.getElementById('my-select');
  const input = document.getElementById('id_first_name');

  mySelect.addEventListener('change', function() {
    if (mySelect.value !== '' || mySelect.value !== null) { 
      input.removeAttribute('disabled');
    } else {
      input.setAttribute('disabled', 'disabled');
    }
  });
});
