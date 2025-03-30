
const destinationName = sessionStorage.getItem("selectedDestination");
const destinationDesc = sessionStorage.getItem("selectedDesc");
const destinationDate = sessionStorage.getItem("selectedTourDate");
console.log("Selected Destination:", destinationName);
console.log("Selected Description:", destinationDesc);
console.log("Selected Date:", destinationDate);

document.getElementById('tour_name').textContent = destinationName;
document.getElementById('tour_desc').textContent = destinationDesc;
document.getElementById('tour_date').textContent = destinationDate;
