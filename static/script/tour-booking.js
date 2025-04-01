document.addEventListener("DOMContentLoaded", function() {
    const destinationName = sessionStorage.getItem("selectedDestination");
    console.log("Selected Destination:", destinationName);

    fetchTourInfo();
    fetchAndDisplayOperators();
    fetchDestinations();
});

async function fetchTourInfo() {
    // Get the selected destination name from sessionStorage
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
        } else {
            // Handle error if destination not found
            console.error(data.error);
            alert('Tour info not found!');
        }
    } catch (error) {
        console.error('Error fetching tour info:', error);
    }
}

async function fetchAndDisplayOperators() {
    const companyName = sessionStorage.getItem("selectedDestination");
   
   try {
       // Fetch tour operators based on company name
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
               <img src="../static/images/location.jpg" alt="${companyName}" width="600">
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
    const destinationName = sessionStorage.getItem("selectedDestination");
    if (!container) return;


    destinations.slice(0, 6).forEach(destination => {
        if (destination.name !== destinationName) {
            const destinationHTML = `
                <div class="destination-content">
                    <img src="/static/images/location.jpg" alt="${destination.name}" width="600">
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
}

document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
        // Check if the clicked element is a "More" button inside an operator-content div
        if (event.target.closest("#to_operator")) {
            const operatorDiv = event.target.closest(".operator-content");

            if (!operatorDiv) return;

            // Get operator details from the DOM
            const operatorData = {
                username: operatorDiv.querySelector("#operator-name")?.innerText || "",
                company_name: operatorDiv.querySelector("#operator-company")?.innerText || "",
                expertise: operatorDiv.querySelector("#expertise")?.innerText || "",
            };

            // Save to sessionStorage
            sessionStorage.setItem("selectedOperator", JSON.stringify(operatorData));

            console.log("Operator saved to sessionStorage:", operatorData);
        }
    });
});