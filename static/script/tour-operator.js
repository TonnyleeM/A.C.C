document.addEventListener("DOMContentLoaded", function () {
    const savedOperator = JSON.parse(sessionStorage.getItem("selectedOperator"));
    if (savedOperator) {
        document.getElementById("tour-name").innerText = savedOperator.username || "Unknown";
        document.getElementById("expertise").innerText = savedOperator.expertise || "No expertise provided";
        document.getElementById("services").innerText = savedOperator.services_offered || "No services listed";
    } else {
        console.error("No operator data found in sessionStorage.");
    }
    fetchOperatorInfo();
    fetchAndDisplayOperators();
});

// Showing operator info on page
async function fetchOperatorInfo() {
    const operatorData = JSON.parse(sessionStorage.getItem("selectedOperator"));
    if (!operatorData) {
        console.error("No operator data found.");
        return;
    }
    const companyName = operatorData.company_name;
    sessionStorage.setItem("selectedDestination", companyName);
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
            sessionStorage.setItem("selectedCountry", data.operators[0].country_name);
            console.log("country:", sessionStorage.getItem("selectedCountry"))
        } else {
            console.error('Unexpected response format:', data);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

async function cacheDetails() {
    try {
    } catch (error) {
        console.error('Error caching info:', error);
    }
}

// Caching tour data and redirecting to tour operator page
document.getElementById("operator-container").addEventListener("click", function (event) {
    if (event.target.closest(".more-btn")) {
        event.preventDefault();
        let operatorContent = event.target.closest(".operator-content");
        let data = {
            username: operatorContent.querySelector("#tour-name").innerText,
            company_name: operatorContent.querySelector("#tour-destination").innerText,
            expertise: operatorContent.querySelector("#expertise").innerText,
            services_offered: operatorContent.querySelector("#expertise").innerText,
            description: "Description not available",
            price: "Price not available",
            duration: "Duration not available",
            country_name: "Country not available"
        };
        sessionStorage.setItem("selectedOperator", JSON.stringify(data));
        console.log("Stored operator data:", data);
        window.location.href = "/tour_operator";
    }
});

// Showing other operators on page
async function fetchAndDisplayOperators() {
    try {
        const response = await fetch('/get_tour_operators_by_country', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        console.log("TOur Operators:", data)
        if (!response.ok) {
            console.error('Error fetching data:', data);
            return;
        }
        const operatorList = document.getElementById('operator-container');
        data.operators.forEach(operator => {
            const operatorContent = document.createElement('div');
            operatorContent.classList.add('operator-content');
            operatorContent.innerHTML = `
                <h3 id="tour-name">${operator.username}</h3>
                <h3 id="tour-destination">${operator.company_name}</h3>
                <p>Expertise in:</p>
                <p id="expertise">${operator.expertise}</p>
                <a class="more-btn" id="to-operator">
                    <button>More</button>
                </a>
            `;
            operatorList.appendChild(operatorContent);
        });
    } catch (error) {
        console.error('Error fetching tour operators:', error);
    }
}