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

            if (data.user.interests && data.user.interests.length > 0) {
                data.user.interests.forEach(interest => {
                    const interestElement = document.createElement('div');
                    interestElement.classList.add('interests-content');
                    const pElement = document.createElement('p');
                    pElement.textContent = interest;
                    interestElement.appendChild(pElement);
                    interestsContainer.appendChild(interestElement);
                });
            } else {
                const noInterestsElement = document.createElement('div');
                noInterestsElement.classList.add('no-interests');
                const noInterestsMessage = document.createElement('p');
                noInterestsMessage.textContent = "No interests are found";
                noInterestsElement.appendChild(noInterestsMessage);
                interestsContainer.appendChild(noInterestsElement);
            }

        } else {
            console.log("Error:", data.message);
        }
    } catch (error) {
        console.log('Error fetching user data:', error);

    }
}

// Log out function
function logout() {
    localStorage.removeItem('userData'); // Remove user data
    localStorage.removeItem("password"); // Reset cached password
    console.log("Cached info reset successfully.");
    window.location.href = '/'; // Redirect to login page
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
        showOverlay(); // Show overlay for delete confirmation
    });
});

// Overlay for delete confirmation
function showOverlay() {
  document.getElementById("deleteOverlay").style.display = "flex";
}

function closeOverlay() {
  document.getElementById("deleteOverlay").style.display = "none";
}

// Handle user confirmation to delete account
async function confirmDelete() {
    const username = localStorage.getItem("username"); // Directly get the username as a string

    if (username) {
        try {
            const response = await fetch('/delete_user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username }) // Send the username to the server
            });

            const data = await response.json();

            if (data.success) {
                console.log('User deleted successfully!');
                // Optionally, log the user out or redirect to a different page
                window.location.href = '/login'; // Redirect to login page or homepage
            } else {
                console.log('Error:', data.message);
            }
        } catch (error) {
            console.log('Error deleting user:', error);
        }
    } else {
        console.log('No user data found in localStorage.');
    }
    // Close the overlay after deletion attempt
    closeOverlay();
    window.location.href = '/';
}
