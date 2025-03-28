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

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("register-btn").addEventListener("click", async function () {
        let username = document.getElementById("username").value.trim();
        console.log(username);
        let password = document.getElementById("password").value;
        console.log(password);
        let email = document.getElementById("email").value.trim();
        console.log(email);
        let phone = document.getElementById("phone").value.trim();
        console.log(phone);
        let interests = "";
        let user_type = document.getElementById("acc-type").value;
        console.log(user_type)
        let errorMessage = document.getElementById("error-message");
        let successMessage = document.getElementById("success-message"); // Element for success messages

        // Clear previous messages
        errorMessage.textContent = "";
        successMessage.textContent = "";

        // Validate required fields
        if (!username || !password || !email || !phone || !user_type) {
            errorMessage.textContent = "All fields except interests are required!";
            return;
        }

        // Prepare data for API
        let userData = { username, password, email, phone, interests, user_type };

        console.log(userData);
        try {
            let response = await fetch("http://127.0.0.1:5000/add_user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            });

            let result = await response.json();

            console.log(result);

            if (result.success === true) {
                successMessage.textContent = "Registration successful!";
                console.log("Registration successful!");
                alert("Registration successful! /n You can now log in with your credentials.");
                // Redirect to login page after a short delay
                setTimeout(() => {
                    window.location.href = "/";
                }, 2000); 
            } else {
                errorMessage.textContent = "Registration failed: " + (result.message || "Unknown error");
                alert("Registration failed: " + (result.message || "Unknown error"));
                console.log("Registration failed: " + (result.message || "Unknown error"));
            }
        } catch (error) {
            console.error("Error:", error);
            console.log("Registration unsuccessful!");
            errorMessage.textContent = "Something went wrong. Please try again!";
        }
    });
});
