// Ensuring password matches password-confirm
document.addEventListener("DOMContentLoaded", () => {
    const password = document.getElementById("password");
    const passwordConfirm = document.getElementById("password-confirm");
    const form = document.querySelector(".login-input");
    const errorMessage = document.getElementById("error-message");

    function validatePasswords() {
        if (password.value !== passwordConfirm.value) {
            errorMessage.textContent = "Passwords do not match!";
            return false;
        } else {
            errorMessage.textContent = "";
            return true;
        }
    }

    password.addEventListener("input", validatePasswords);
    passwordConfirm.addEventListener("input", validatePasswords);

    form.addEventListener("submit", (event) => {
        if (!validatePasswords()) {
            event.preventDefault();
        }
    });
});

// Toggling password visibility
function togglePassword(id) {
    const input = document.getElementById(id);
    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}

