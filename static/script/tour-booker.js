document.addEventListener("DOMContentLoaded", function () {
    const destinationName = sessionStorage.getItem("selectedDestination") || "Unknown";
    const destinationDesc = sessionStorage.getItem("selectedDesc") || "No description available.";

    console.log("Selected Destination:", destinationName);
    console.log("Selected Description:", destinationDesc);

    document.getElementById('location-name').textContent = destinationName;
    document.getElementById('location-desc').textContent = destinationDesc;

    if (destinationName !== "Unknown") {
        fetchPrice(destinationName);
    }

    document.getElementById('book-btn').addEventListener('click', function () {
        const selectedTourDate = document.getElementById('booking-date').value;
        sessionStorage.setItem("selectedTourDate", selectedTourDate);
        console.log("Tour Date saved to sessionStorage:", selectedTourDate);
        window.location.href = '/tour_confirm';
    });

    document.getElementById('back').addEventListener('click', function () {
        window.location.href = '/tour-booking';
    });

    async function fetchPrice(destinationName) {
        console.log("Fetching user and pricing data...");

        try {
            const response = await fetch(`/get_price`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ destinationName }),
            });

            const data = await response.json();
            console.log("Received data:", data);

            if (data) {
                const priceElement = document.getElementById("location-price");
                priceElement.innerText = data[0];
                sessionStorage.setItem("selectedTourPrice", data[0]);

            } else {
                console.error("Error:", data.message);
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
        }
    }
});
