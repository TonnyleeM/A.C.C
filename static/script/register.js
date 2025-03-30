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
    document.getElementById("register-btn").addEventListener("click", async function (event) {
        event.preventDefault(); 
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
        console.log(user_type);

        // Validate required fields
        if (!username || !password || !email || !phone || !user_type) {
            alert("All fields except interests are required!");
            console.log("All fields except interests are required!");
            return;
        }

        // Prepare data for API
        let userData = { username, password, email, phone, interests, user_type };

        console.log(userData);

        // If user type is 'operator', store the user data in cache and redirect
        if (user_type === "operator") {
            // Save the user data to cache (localStorage)
            localStorage.setItem("tempUserData", JSON.stringify(userData));
            localStorage.setItem("username", username);
            console.log("Operator user data cached. Redirecting...");
            // Redirect to operator login page
            window.location.href = "/operator_login";

        } else {
            // If user type is not 'operator', proceed with saving to the database
            try {
                let response = await fetch("/add_user", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(userData)
                });

                let result = await response.json();
                console.log("Result: ", result);

                if (result.success === false) {
                    alert("Registration failed: " + (result.message || "Unknown error"));
                    console.log("Registration failed: " + (result.message || "Unknown error"));
                } else {
                    console.log("Registration successful!");
                    alert("Registration successful! \nYou can now log in with your credentials.");
                    setTimeout(() => {
                        window.location.href = "/";
                    }, 2000); 
                }
            } catch (error) {
                console.error("Error:", error);
                console.log("Registration unsuccessful!");
                alert("Something went wrong. Please try again!");
            }
        }
    });
});
