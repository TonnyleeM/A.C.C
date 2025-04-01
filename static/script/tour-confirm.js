const destinationName = sessionStorage.getItem("selectedDestination");
const destinationDesc = sessionStorage.getItem("selectedDesc");
const destinationDate = sessionStorage.getItem("selectedTourDate");
const destinationPrice = sessionStorage.getItem("selectedTourPrice")
console.log("Selected Destination:", destinationName);
console.log("Selected Description:", destinationDesc);
console.log("Selected Date:", destinationDate);
console.log("Local Storage (JSON):", JSON.stringify(localStorage, null, 2));
console.log("Session Storage (JSON):", JSON.stringify(sessionStorage, null, 2));

document.getElementById('tour_name').textContent = destinationName;
document.getElementById('tour_desc').textContent = destinationDesc;
document.getElementById('tour_date').textContent = destinationDate;
document.getElementById('tour_price').textContent = destinationPrice;

// Saving booking to database
document.addEventListener("DOMContentLoaded", function() {
    document.addEventListener("click", function (event) {
        if (event.target.closest("#to-confirm")) {
            const username = localStorage.getItem("username");
            const tourName = sessionStorage.getItem("selectedDestination");
            const tourDate = sessionStorage.getItem("selectedTourDate");
            const tourPrice = sessionStorage.getItem("selectedTourPrice");
            if (!username || !tourName || !tourDate || !tourPrice) {
                console.error("Missing required booking information.");
                return;
            }
            fetch("/book_tour", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    tour_name: tourName,
                    booking_date: tourDate,
                    total_cost: parseFloat(tourPrice),
                    status: "pending"
                })
            })
            .then(response => response.json())
            .then(data => console.log("Booking response:", data))
            .then(alert("Booking Successful"))
            .catch(error => console.error("Error:", error));
        }
    });
});
