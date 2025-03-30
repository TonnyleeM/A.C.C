// Retrieve the username from localStorage
let username = localStorage.getItem("username");
if (username) {
  console.log("Logged in as:", username);

} else {
  console.log("User not logged in.");
  alert("User logged out unexpectedly, Redirecting to login page")
  window.location.href = '/';
}

let userData = JSON.parse(localStorage.getItem("tempUserData")); ;
console.log("User Data from LocalStorage:", userData);


document.getElementById("country-name").addEventListener("change", function() {
    const selectedCountry = this.value;
    console.log("Selected country:", selectedCountry)
    if (selectedCountry) {
        fetch('/get_tours', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                country_name: selectedCountry
            })
        })
            .then(response => response.json())
            .then(data => {
                const companySelect = document.getElementById("company-name");
                console.log("Data:", data)
                companySelect.innerHTML = '<option value="" disabled selected>Select Destination</option>'; // Reset the options
                if (data.length > 0) {
                    data.forEach(destination => {
                        const option = document.createElement("option");
                        option.value = destination.destination_id;  // Corrected key access
                        option.textContent = destination.name;  // destination name
                        companySelect.appendChild(option);
                    });
                } else {
                    const noOption = document.createElement("option");
                    noOption.textContent = "No destinations available";
                    companySelect.appendChild(noOption);
                }
            })
            .catch(error => {
                console.error("Error fetching destinations:", error);
            });
    } else {
        const companySelect = document.getElementById("company-name");
        companySelect.innerHTML = '<option value="" disabled selected>Select Country First</option>';  // Reset if no country is selected
    }
});


document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("button").addEventListener("click", async function () {
        const country = document.getElementById("country-name").value;
        const company = document.getElementById("company-name").value;
        const expertise = document.getElementById("expertise").value.trim();
        const serviceOffered = document.getElementById("service-offered").value.trim();

        if (!country || !company || !expertise || !serviceOffered) {
            alert("Please fill in all fields before saving.");
            return;
        }

        const data = {
            country: country,
            company: company,
            expertise: expertise,
            services_offered: serviceOffered
        };
        
        try {
            // Send user data first
            let response = await fetch("/add_user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)  // Change to 'data'
            });

            let result = await response.json();
            console.log("Result from add_user:", result);

            if (result.success) {
                const userId = result.user_id;  // Get user_id from the response
                data.user_id = userId;  // Add user_id to the operator data
                console.log("user_id:", data.user_id);

                // After adding user data, save operator data
                let operatorResponse = await fetch("/save_operator", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                });

                let operatorResult = await operatorResponse.json();
                alert(operatorResult.message);
                console.log("Operator save result:", operatorResult);
                console.log(data)
                window.location.href = '/';  // Redirect to home page
            } else {
                alert("Failed to create user.");
            }

        } catch (error) {
            console.error("Error saving information:", error);
            alert("Failed to save information.");
        }
    });
});



