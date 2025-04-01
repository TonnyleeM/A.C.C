document.addEventListener("DOMContentLoaded", function() {
    const destinationName = sessionStorage.getItem("selectedCountry");
    console.log("Selected Destination:", destinationName);
    fetchAndDisplayOperators();
});

// Showing operator info on page
async function fetchAndDisplayOperators() {
    try {
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
        const operatorList = document.getElementById('destination-container');
        operatorList.innerHTML = '';
        data.operators.forEach(operator => {
            const operatorContent = document.createElement('div');
            operatorContent.classList.add('destination-content');
            operatorContent.innerHTML = `
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

// Caching tour details
document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
        if (event.target.closest("#to-operator")) {
            const operatorDiv = event.target.closest(".destination-content");
            if (!operatorDiv) return;
            const operatorData = {
                username: operatorDiv.querySelector("#tour-name")?.innerText || "",
                company_name: operatorDiv.querySelector("#tour-destination")?.innerText || "",
                expertise: operatorDiv.querySelector("#expertise")?.innerText || "",
            };
            sessionStorage.setItem("selectedOperator", JSON.stringify(operatorData));
            console.log("Operator saved to sessionStorage:", operatorData);
        }
    });
});