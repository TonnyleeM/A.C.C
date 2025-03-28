// Retrieve the username from localStorage
let username = localStorage.getItem("username");
if (username) {
  console.log("Logged in as:", username);

} else {
  console.log("User not logged in.");
}

// Clear the username from localStorage when logging out
localStorage.removeItem("username");