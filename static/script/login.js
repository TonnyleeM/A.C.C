localStorage.removeItem('userData');
localStorage.removeItem("password");
console.log("Cached info reset successfully.");

function togglePassword(id) {
  const input = document.getElementById(id);
  if (input.type === "password") {
      input.type = "text";
  } else {
      input.type = "password";
  }
}


// Logging into account
document.addEventListener("DOMContentLoaded", function () {
  document.querySelector(".login-input").addEventListener("submit", async function (event) {
      event.preventDefault();
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
          localStorage.setItem("username", result.username);
          localStorage.setItem("password", result.password);
          console.log("Logged in as:", result.username);
          window.location.href = "/homepage";
      } else {
          alert("Invalid username or password");
      }
  });
});
