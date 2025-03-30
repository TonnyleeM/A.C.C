// Retrieve the username from localStorage
let username = localStorage.getItem("username");
if (username) {
  console.log("Logged in as:", username);

} else {
  console.log("User not logged in.");
  alert("User logged out unexpectedly, Redirecting to login page")
  window.location.href = '/'; // Redirect to login page if not logged in
}

window.onload = function() {
    const username = localStorage.getItem("username")
    const password = localStorage.getItem("password")
    // Call fetchUserData when the page loads
    fetchUserData(username, password);
    fetchEmployer(username);
};

 // Fetch user data from API
async function fetchUserData(username, password) {
    console.log("Searching for user data...")
    try {
        const response = await fetch(`/get_user`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();

        if (data.success) {
            usernameElement = document.querySelector('#user-name');
            const interestsContainer = document.getElementById("interests-container");
            usernameElement.innerText = data.user.username;
            document.getElementById("user-type").innerText = data.user.userType;
            interestsContainer.innerHTML = "";
            console.log("User data found")
        } else {
            console.log("Error:", data.message);
        }

    } catch (error) {
        console.log('Error fetching user data:', error);

    }
}

async function fetchEmployer(username) {
    console.log("Searching for user data...")
    try {
        const response = await fetch(`/load_operator`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username }),
        });
        const data = await response.json();
        console.log("Found databia:", data)
        if (data) {
            usernameElement = document.getElementById('employer-name');
            usernameElement.innerText = data[3];
            console.log("Operator data found")
        } else {
            console.log("Error:", data.message);
        }

    } catch (error) {
        console.log('Error fetching user data:', error);

    }
    
}
// Log out function
function logout() {
    sessionStorage.clear();
    localStorage.clear();
    console.log("Cached info reset successfully.");
    window.location.href = '/'; 
}

// Wait for DOM to load before adding event listeners
document.addEventListener("DOMContentLoaded", () => {
    const logoutButton = document.getElementById("logoutbutton");
    const deleteButton = document.getElementById("deletebutton");

    logoutButton.addEventListener('click', (e) => {
        e.preventDefault();
        logout();
    });

    deleteButton.addEventListener('click', (e) => {
        e.preventDefault();
        showOverlay();
    });
});

function showOverlay() {
  document.getElementById("deleteOverlay").style.display = "flex";
}

function closeOverlay() {
  document.getElementById("deleteOverlay").style.display = "none";
}

// Handle user confirmation to delete account
async function confirmDelete() {
    const username = localStorage.getItem("username"); 

    if (username) {
        try {
            const response = await fetch('/delete_user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username })
            });

            const data = await response.json();

            if (data.success) {
                sessionStorage.clear();
                localStorage.clear();
                console.log('User deleted successfully!');
                
                window.location.href = '/login';
            } else {
                console.log('Error:', data.message);
            }
        } catch (error) {
            console.log('Error deleting user:', error);
        }
    } else {
        console.log('No user data found in localStorage.');
    }
    closeOverlay();
    window.location.href = '/';
}
