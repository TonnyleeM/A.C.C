document.addEventListener("DOMContentLoaded", () => {
    const storedCountry = sessionStorage.getItem("selectedCountry");

    if (storedCountry) {
        console.log("Retrieved country:", storedCountry);

        const countryNameElements = document.querySelectorAll(".country-name"); // Use class instead of ID
        const countryFlagElement = document.getElementById("country-flag");

        // Update all elements with class 'country-name'
        countryNameElements.forEach(element => {
            element.innerText = storedCountry;
        });

        if (countryFlagElement) {
            const countryFlag = `${storedCountry.toLowerCase().replace(/\s+/g, '-')}-flag.jpg`; 
            countryFlagElement.src = `/static/images/${countryFlag}`;

            // Handle missing images
            countryFlagElement.onerror = () => {
                countryFlagElement.src = "/static/images/default-flag.jpg";
            };
        }

        // Fetch additional country data
        fetchCountryData(storedCountry);
        fetchDestinations(storedCountry);
        
    }
});

// Function to fetch country data (Ensure this is in scope before usage)
async function fetchCountryData(selectedCountry) {
    if (!selectedCountry) {
        console.error("No country selected.");
        return;
    }

    try {
        const response = await fetch('/get_country', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selectedCountry: selectedCountry.trim() })
        });

        const data = await response.json();

        if (data.success) {
            console.log('Country Data:', data.user);
            
            const countryNameElement = document.getElementById('country-name');
            const countryInfoElement = document.getElementById('country-info');

            if (countryNameElement) countryNameElement.textContent = data.user.country_name;
            if (countryInfoElement) countryInfoElement.textContent = data.user.description;

            // Get the iframe element to update the map URL dynamically
            const countryMapIframe = document.getElementById('country-map-iframe');

            if (countryMapIframe) {
                const countryMapURL = data.user.map_url;  // The map URL returned from the server
                countryMapIframe.src = countryMapURL;    // Set the src to the map URL
            }
        } else {
            console.error('Error:', data.message);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

// Fetch destinations and update UI
async function fetchDestinations(selectedCountry) {
    if (!selectedCountry) {
        console.error("No country selected.");
        return;
    }

    try {
        
        const response = await fetch('/get_tours', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ country_name: selectedCountry })
        });

        const data = await response.json();
        console.log(data)
        if (Array.isArray(data)) {  // Since API directly returns an array
            console.log('Destinations:', data);
            displayDestinations(data);
        } else {
            console.error('Unexpected response:', data);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

function displayDestinations(destinations) {
    const container = document.querySelector(".destination-container");
    if (!container) return;

    // container.innerHTML = ""; Clear existing content

    destinations.slice(0, 6).forEach(destination => {
        const destinationHTML = `
            <div class="destination-content">
                <h3>${destination.name}</h3>
                <p>${destination.description}</p>
                <a href="/tour-booking">
                    <button class="button" onclick="cacheDestinationName('${destination.name}')">More</button>
                </a>
            </div>
        `;
        container.innerHTML += destinationHTML;
    });
}

// Function to cache the destination name
function cacheDestinationName(destinationName) {
    // Store the destination name in sessionStorage or localStorage
    sessionStorage.setItem("selectedDestination", destinationName);
    console.log("Selected Destination:", destinationName);
}
