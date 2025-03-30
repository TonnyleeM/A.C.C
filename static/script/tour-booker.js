document.addEventListener("DOMContentLoaded", function() {
    const destinationName = sessionStorage.getItem("selectedDestination");
    console.log("Selected Destination:", destinationName);
    const destinationDesc = sessionStorage.getItem("selectedDesc");
    console.log("Selected Description:", destinationDesc);

    document.getElementById('location-name').textContent = destinationName;
    document.getElementById('location-desc').textContent = destinationDesc;

    document.getElementById('book-btn').addEventListener('click', function() {
        const selectedTourDate = document.getElementById('booking-date').value;

        sessionStorage.setItem("selectedTourDate", selectedTourDate);
        console.log("Tour Date saved to sessionStorage:", selectedTourDate);
    });
});
