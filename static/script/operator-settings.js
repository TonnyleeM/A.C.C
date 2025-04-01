// Retrieve the username from localStorage
let username = localStorage.getItem("username");
if (username) {
  console.log("Logged in as:", username);
} else {
  console.log("User not logged in.");
  alert("User logged out unexpectedly, Redirecting to login page")
  window.location.href = '/'; // Redirect to login page if not logged in
}

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
            usernameElement.innerText = data.user.username;
            document.getElementById("user-type").innerText = data.user.userType;
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
        console.log("Found data:", data)
        if (data) {
            usernameElement = document.getElementById('employer-name');
            usernameElement.innerText = data[3];
            console.log("Operator data found", data[3])
            sessionStorage.setItem("company_name", data[3])
        } else {
            console.log("Error:", data.message);
        }

    } catch (error) {
        console.log('Error fetching user data:', error);
    }
}

// Fetch bookings
function fetchBookings() {
    const companyName = sessionStorage.getItem("company_name");
    const bookingsContainer = document.getElementById("bookings-container");

    fetch("/show_bookings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company_name: companyName })
    })
    .then(response => response.json())
    .then(data => {
        bookingsContainer.innerHTML = "";
        console.log("Bookings found: ", data)
        if (data.error) {
            bookingsContainer.innerHTML = `<p>${data.error}</p>`;
            return;
        }
        
        data.bookings.forEach(booking => {
            const bookingDiv = document.createElement("div");

            bookingDiv.innerHTML = `
                <div class="booking-content">
                    <p>Username: ${booking.username}</p>
                    <p>Booking Date: ${booking.booking_date}</p>
                    <p>Price: USD${booking.total_cost}</p>
                    <p>Status: ${booking.status}</p>
                    <button class="accept-btn" data-id="${booking.booking_id}">Accept</button>
                    <button class="reject-btn" data-id="${booking.booking_id}">Reject</button>
                </div>
            `;
            bookingsContainer.appendChild(bookingDiv);
        });

        // Add event listeners to accept/reject buttons after the bookings are rendered
        const acceptButtons = document.querySelectorAll(".accept-btn");
        const rejectButtons = document.querySelectorAll(".reject-btn");

        acceptButtons.forEach(button => {
            button.addEventListener("click", (e) => {
                const bookingId = e.target.getAttribute("data-id");
                acceptBooking(bookingId);
            });
        });

        rejectButtons.forEach(button => {
            button.addEventListener("click", (e) => {
                const bookingId = e.target.getAttribute("data-id");
                rejectBooking(bookingId);
            });
        });

    })
    .catch(error => {
        bookingsContainer.innerHTML = `<p>Error loading bookings.</p>`;
    });
}


async function acceptBooking(bookingId) {
    try {
        const response = await fetch('/accept_booking', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ booking_id: bookingId })
        });
        const data = await response.json();
        if (data.message) {
            alert(data.message); // Show success message
            fetchBookings(); // Refresh the bookings list
        } else {
            alert(data.error); // Show error message
        }
    } catch (error) {
        alert("Error accepting booking.");
    }
}

// Function to call the reject booking API
async function rejectBooking(bookingId) {
    try {
        const response = await fetch('/reject_booking', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ booking_id: bookingId })
        });
        const data = await response.json();
        if (data.message) {
            alert(data.message); // Show success message
            fetchBookings(); // Refresh the bookings list
        } else {
            alert(data.error); // Show error message
        }
    } catch (error) {
        alert("Error rejecting booking.");
    }
}


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

// Wait for DOM to load and then execute the functions
window.onload = async function() {
    const password = localStorage.getItem("password");
    await fetchUserData(username, password);
    await fetchEmployer(username);
    fetchBookings();  // Now fetchBookings runs after fetchEmployer
};
