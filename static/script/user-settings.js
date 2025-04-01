// Retrieve the username from localStorage
let username = localStorage.getItem("username");
if (username) {
  console.log("Logged in as:", username);

} else {
  console.log("User not logged in.");
  alert("User logged out unexpectedly, Redirecting to login page")
  window.location.href = '/';
}

window.onload = function() {
    const username = localStorage.getItem("username")
    const password = localStorage.getItem("password")
    
    fetchUserData(username, password);
    showBookings();
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
        console.log("Recieved data for Settings: ",data)
        if (data.success) {
            usernameElement = document.querySelector('#user-name');
            const interestsContainer = document.getElementById("interests-container");
            usernameElement.innerText = data.user.username;
            document.getElementById("user-type").innerText = data.user.userType;
            interestsContainer.innerHTML = "";
            if (data.user.userType === "operator") {
                window.location.href = '/operator_settings';
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
    localStorage.removeItem('userData'); 
    localStorage.removeItem("password"); 
    console.log("Cached info reset successfully.");
    window.location.href = '/'; 
}


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

// Showing the bookings for a user
async function showBookings() {
    const username = localStorage.getItem("username");

    try {
        const response = await fetch(`/show_tour`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username }),
        });

        if (!response.ok) {
            console.error('Error fetching bookings:', response.statusText);
            return;
        }

        const data = await response.json();
        console.log("Received Data:", data);

        if (data.error) {
            console.error('Error:', data.error);
            return;
        }

        const container = document.querySelector(".interests-container");
        if (!container) return;

        container.innerHTML = ""; 

        data.bookings.forEach(booking => {
            const bookingHTML = `
                <div class="booking-content">
                    <h3>${booking.tour_name}</h3>
                    <p>Booking Date: ${booking.booking_date}</p>
                    <p>Status: ${booking.status}</p>
                    <p>Total Cost: $${booking.total_cost}</p>
                </div>
            `;
            container.innerHTML += bookingHTML;
        });

    } catch (error) {
        console.error('Error fetching bookings:', error);
    }
}