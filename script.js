document.addEventListener("DOMContentLoaded", function() {
    const searchBtn = document.getElementById("search-btn");
    const resultsContainer = document.getElementById("results-container");

    // Add event listener to each input field for Enter key
    document.querySelectorAll("input").forEach(input => {
        input.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();  // Prevents form submission
                fetchResults();
            }
        });
    });

    searchBtn.addEventListener("click", fetchResults);

function fetchResults() {
    const firstNameInput = document.getElementById("first-name");
    const lastNameInput = document.getElementById("last-name");
    const jobTitleInput = document.getElementById("job-title");
    const companyNameInput = document.getElementById("company-name");
    const resultsContainer = document.getElementById("results-container");

    let queryParams = new URLSearchParams({
        first_name: firstNameInput.value.trim(),
        last_name: lastNameInput.value.trim(),
        title: jobTitleInput.value.trim(),
        company: companyNameInput.value.trim()
    });

    fetch(`/search?${queryParams.toString()}`)
        .then(res => res.json())
        .then(data => {
            resultsContainer.innerHTML = "";

            if (data.message) {
                resultsContainer.innerHTML = `<p>${data.message}</p>`;
                return;
            }

            data.forEach(employee => {
                const resultItem = document.createElement("div");
                resultItem.className = "result-item";
                resultItem.innerHTML = `
                    <strong>${employee.name}</strong>
                    <span class="company-name"><em>${employee.company}</em></span>
                    <span class="job-title"> | ${employee.title}</span>
                `;
                resultsContainer.appendChild(resultItem);
            });

            // **Clear input fields after search**
            firstNameInput.value = "";
            lastNameInput.value = "";
            jobTitleInput.value = "";
            companyNameInput.value = "";
        })
        .catch(error => console.error("Error fetching search results:", error));
}
});
