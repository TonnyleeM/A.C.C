document.addEventListener("DOMContentLoaded", () => {
    const countryButtons = document.querySelectorAll(".button");

    countryButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            const countryName = event.target.closest(".location-content").querySelector("#country-name").innerText;
            sessionStorage.setItem("selectedCountry", countryName);
            console.log("Country cached:", countryName);
        });
    });
});
