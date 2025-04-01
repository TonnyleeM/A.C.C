document.addEventListener("DOMContentLoaded", function () {
    // Retrieve operator data from sessionStorage
    const savedOperator = JSON.parse(sessionStorage.getItem("selectedOperator"));

    if (savedOperator) {
        // Update HTML elements with the stored data
        document.getElementById("tour-name").innerText = savedOperator.username || "Unknown";
        document.getElementById("expertise").innerText = savedOperator.expertise || "No expertise provided";
        document.getElementById("services").innerText = savedOperator.services_offered || "No services listed";
    } else {
        console.error("No operator data found in sessionStorage.");
    }
    
    fetchOperatorInfo();
    fetchAndDisplayOperators();

});

async function fetchOperatorInfo() {
    const operatorData = JSON.parse(sessionStorage.getItem("selectedOperator"));

    if (!operatorData) {
        console.error("No operator data found.");
        return;
    }

    const companyName = operatorData.company_name;
    console.log("Cached company name:", companyName);

    try {
        const response = await fetch('/get_tour_operators', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ company_name: companyName })
        });

        const data = await response.json();
        console.log("Response data:", data);

        if (data.operators && Array.isArray(data.operators)) {  
            console.log('Destinations:', data.operators);
            document.getElementById("services").innerText = data.operators[0].services_offered;

            document.getElementById("location-name").innerText = data.operators[0].company_name;
            document.getElementById("location-desc").innerText = data.operators[0].description;
            document.getElementById("location-price").innerText = data.operators[0].price;
            document.getElementById("location-duration").innerText = data.operators[0].duration;
        } else {
            console.error('Unexpected response format:', data);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

async function fetchAndDisplayOperators() {
    try {
        // Fetch tour operators without sending any data
        const response = await fetch('/get_tour_operators_by_country', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (!response.ok) {
            console.error('Error fetching data:', data);
            return;
        }

        // Assuming you want to insert this information into a container with the id 'destination-container'
        const operatorList = document.getElementById('operator-container');
        // Iterate through operators and create the HTML
        data.operators.forEach(operator => {
            // Create the operator content dynamically
            const operatorContent = document.createElement('div');
            operatorContent.classList.add('operator-content');
            
            operatorContent.innerHTML = `
                <img src="/static/images/location.jpg" alt="${operator.company_name}" width="600">
                <h3 id="tour-name">${operator.username}</h3>
                <h3 id="tour-destination">${operator.company_name}</h3>
                <p>Expertise in:</p>
                <p id="expertise">${operator.expertise}</p>
                <a href="/tour_operator" class="more-btn" id="to-operator">
                    <button>More</button>
                </a>
            `;

            operatorList.appendChild(operatorContent);
        });

    } catch (error) {
        console.error('Error fetching tour operators:', error);
    }
}