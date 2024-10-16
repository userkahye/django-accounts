const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');

togglePassword.addEventListener('click', function () {
  // Toggle the type attribute
  const type = passwordInput.type === 'password' ? 'text' : 'password';
  passwordInput.type = type;

  // Toggle the correct eye icon
  this.textContent = type === 'password' ? 'visibility_off' : 'visibility';
});

// Handle form submission via AJAX
document.getElementById('registrationForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent normal form submission

  // Clear previous error and success messages
  document.getElementById('usernameError').textContent = '';
  document.getElementById('emailError').textContent = '';
  document.getElementById('passwordError').textContent = '';
  document.getElementById('successMessage').textContent = '';

  const formData = new FormData(this);

  fetch("{% url 'register' %}", {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Show success message
        document.getElementById('successMessage').textContent = data.message;
        setTimeout(() => {
          window.location.href = data.redirect_url;
        }, 7000); // Redirect after 7secs.
      } else {
        // Display errors under each field
        if (data.errors.username) {
          document.getElementById('usernameError').textContent = data.errors.username[0];
        }
        if (data.errors.email) {
          document.getElementById('emailError').textContent = data.errors.email[0];
        }
        if (data.errors.password) {
          document.getElementById('passwordError').textContent = data.errors.password[0];
        }
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
});
