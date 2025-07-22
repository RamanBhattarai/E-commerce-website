function validatePasswords() {
      const pass = document.getElementById("password").value;
      const confirm = document.getElementById("confirm_password").value;
      const errorMsg = document.getElementById("error-message");

      if (pass !== confirm) {
        errorMsg.style.display = "block";
        errorMsg.innerText = "Passwords do not match!";
        return false;
      }
      errorMsg.style.display = "none";
      return true;
    }

function togglePassword(id, iconElement) {
      const input = document.getElementById(id);
      if (input.type === "password") {
        input.type = "text";
        iconElement.textContent = "🙈";
      } else {
        input.type = "password";
        iconElement.textContent = "👁️";
      }
    }