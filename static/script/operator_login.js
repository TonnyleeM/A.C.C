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
                companySelect.innerHTML = '<option value="" disabled selected>Select Destination</option>';
                if (data.length > 0) {
                    data.forEach(destination => {
                        const option = document.createElement("option");
                        option.textContent = destination.name;
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
        companySelect.innerHTML = '<option value="" disabled selected>Select Country First</option>';
    }
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#back").addEventListener("click", async function () {
        window.history.back();      
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#save-info").addEventListener("click", async function () {
        const country = document.getElementById("country-name").value;
        const company = document.getElementById("company-name").value;
        const tourPrice = document.getElementById("tour_price").value;
        const tourDate = document.getElementById("tour_date").value;
        const expertise = document.getElementById("expertise").value.trim();
        const serviceOffered = document.getElementById("service-offered").value.trim();

        if (!country || !company || !expertise || !serviceOffered || !tourPrice || !tourDate) {
            alert("Please fill in all fields before saving.");
            return;
        }

        console.log("Company name:", company);

        const user_info = {
            country: country,
            company_name: company,
            expertise: expertise,
            services_offered: serviceOffered,
            tour_date: tourDate,
            tour_price: tourPrice
        };

        console.log("Tour info:", user_info);
        console.log("User info:", userData);
        try {
            let response = await fetch("/add_user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)  
            });

            let data_result = await response.json();
            console.log("Result from add_user:", data_result);

            if (data_result.success) {
                const userId = data_result.user_id;  
                user_info.user_id = userId;  
                console.log("user_id:", user_info.user_id);

                let operatorResponse = await fetch("/save_operator", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(user_info) 
                });

                let operatorResult = await operatorResponse.json();
                alert(operatorResult.message);
                operator_id = operatorResult.operator_id;
                
                console.log("Operator save result:", operatorResult);

                let tourResponse = await fetch("/save_tour_info", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(user_info) 
                });

                let tourResult = await tourResponse.json();
                alert(tourResult.message);
                console.log("Tour save result:", tourResult);

                window.location.href = '/'; 
            } else {
                alert("Failed to create user, ",operatorResult);
            }
        } catch (error) {
            console.error("Error saving information:", error);
            alert("Failed to save information.");
        }
    });
});