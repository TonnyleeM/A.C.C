// Toggling password visibility
function togglePassword(id) {
  const input = document.getElementById(id);
  if (input.type === "password") {
      input.type = "text";
  } else {
      input.type = "password";
  }
}

// Login credentials validation
document.addEventListener("DOMContentLoaded", function () {
  document.querySelector(".login-input").addEventListener("submit", async function (event) {
      event.preventDefault(); // Prevent default form submission

      let username = document.getElementById("username").value;
      let password = document.getElementById("password").value;

      let response = await fetch("/login_check", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({ username: username, password: password })
      });

      let result = await response.json();
      if (result.success) {
          alert("Login successful!");
          window.location.href = "/homepage"; // Redirect user after successful login
      } else {
          alert("Invalid username or password");
      }
  });
});
