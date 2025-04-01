document.addEventListener("DOMContentLoaded", function() {
    const destinationName = sessionStorage.getItem("selectedCountry");
    console.log("Selected Destination:", destinationName);
    fetchAndDisplayOperators();
});

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
        const operatorList = document.getElementById('destination-container');
        operatorList.innerHTML = ''; // Clear existing content

        // Iterate through operators and create the HTML
        data.operators.forEach(operator => {
            // Create the operator content dynamically
            const operatorContent = document.createElement('div');
            operatorContent.classList.add('destination-content');
            
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

document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
        // Check if the clicked element is a "More" button inside an operator-content div
        if (event.target.closest("#to-operator")) {
            const operatorDiv = event.target.closest(".destination-content");

            if (!operatorDiv) return;

            // Get operator details from the DOM
            const operatorData = {
                username: operatorDiv.querySelector("#tour-name")?.innerText || "",
                company_name: operatorDiv.querySelector("#tour-destination")?.innerText || "",
                expertise: operatorDiv.querySelector("#expertise")?.innerText || "",
            };

            // Save to sessionStorage
            sessionStorage.setItem("selectedOperator", JSON.stringify(operatorData));

            console.log("Operator saved to sessionStorage:", operatorData);
        }
    });
});