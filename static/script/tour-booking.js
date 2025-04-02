document.addEventListener("DOMContentLoaded", function() {
    const destinationName = sessionStorage.getItem("selectedDestination");
    console.log("Selected Destination:", destinationName);
    fetchTourInfo();
    fetchAndDisplayOperators();
    fetchDestinations();
});

// Fetching and displaying tour Info
async function fetchTourInfo() {
    const destinationName = sessionStorage.getItem("selectedDestination");
    if (!destinationName) {
        console.error("Destination name not found in sessionStorage");
        alert("Destination not selected!");
        return;
    }
    try {
        const response = await fetch('/get_tour_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ destinationName })
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById('location-name').textContent = data[2];
            document.getElementById('location-desc').textContent = data[3];
            sessionStorage.setItem('selectedDesc', data[3])
            console.log('GetTouInfo response:', data)
            const location_container = document.getElementById('location-map-container');
            location_container.innerHTML = '';
            const operatorContent = document.createElement('div');
            operatorContent.classList.add('location-map-content');
            operatorContent.innerHTML = `
              <iframe src="${data[4]}" title="Location Map" <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d18967.87467894157!2d30.133535040817836!3d-1.9514213092365928!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x19dca796f9417ad5%3A0x45ebba72296bfee2!2sKigali%20International%20Airport!5e0!3m2!1sen!2srw!4v1743516538430!5m2!1sen!2srw" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
           `;
           location_container.appendChild(operatorContent);
           console.log(data[5])
           document.getElementById("location-image").src = data[5];
            console.log('Location URL:', data[4]);
        } else {
            console.error(data.error);
            alert('Tour info not found!');
        }
    } catch (error) {
        console.error('Error fetching tour info:', error);
    }
}

// Fetching and displaying operators
async function fetchAndDisplayOperators() {
    const companyName = sessionStorage.getItem("selectedDestination");
    try {
        const response = await fetch('/get_tour_operators', {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json'
            },
            body: JSON.stringify({ company_name: companyName })
        });
        const data = await response.json();
        if (!response.ok) {
            console.error('Error fetching data:', data.error);
            return;
        }
        const operatorList = document.getElementById('operator-list');
        operatorList.innerHTML = '';
        data.operators.forEach(operator => {
            const operatorContent = document.createElement('div');
            operatorContent.classList.add('operator-content');
            operatorContent.innerHTML = `
                <h3 id="operator-name">${operator.username}</h3>
                <h3 id="operator-company">${operator.company_name}</h3>
                <p>Expertise in:</p>
                <p id="expertise">${operator.expertise}</p>
                <a href="/tour_operator" class="more-btn">
                    <button id="to_operator">More</button>
                </a>
            `;
            operatorList.appendChild(operatorContent);
        });
    } catch (error) {
        console.error('Error fetching tour operators:', error);
    }
}

// Fetching destinations from database
async function fetchDestinations(selectedCountry) {
    const storedCountry = sessionStorage.getItem("selectedCountry");
    console.log("Cached country:", storedCountry);
    if (!storedCountry) {
        console.error("No country selected.");
        return;
    }
    try {
        const response = await fetch('/get_tours', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ country_name : storedCountry })
        });
        const data = await response.json();
        console.log("Destinations:",data)
        if (Array.isArray(data)) {  
            displayDestinations(data);
        } else {
            console.error('Unexpected response:', data);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

// Displaying destinations to page
function displayDestinations(destinations) {
    const container = document.querySelector(".destination-container");
    const destinationName = sessionStorage.getItem("selectedDestination");
    if (!container) return;

    destinations.slice(0, 6).forEach(destination => {
        if (destination.name !== destinationName) {
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
        }
    });
}4

// Caching operator info
document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
        if (event.target.closest("#to_operator")) {
            const operatorDiv = event.target.closest(".operator-content");
            if (!operatorDiv) return;
            const operatorData = {
                username: operatorDiv.querySelector("#operator-name")?.innerText || "",
                company_name: operatorDiv.querySelector("#operator-company")?.innerText || "",
                expertise: operatorDiv.querySelector("#expertise")?.innerText || "",
            };
            sessionStorage.setItem("selectedOperator", JSON.stringify(operatorData));
            console.log("Operator saved to sessionStorage:", operatorData);
        }
    });
});

function cacheDestinationName(destination) {
    sessionStorage.setItem("selectedDestination", destination);
}