document.addEventListener("DOMContentLoaded", function () {
    const searchBtn = document.getElementById("search-btn");
    const searchInput = document.getElementById("search-input");
    const suggestionsDiv = document.getElementById("suggestions");
    const employeeDetailsDiv = document.getElementById("employee-details");

    searchBtn.addEventListener("click", fetchResults);

    function fetchResults() {
        const query = searchInput.value.trim();

        if (!query) {
            suggestionsDiv.innerHTML = "<p>Please enter a search query.</p>";
            return;
        }

        fetch(`/search?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestionsDiv.innerHTML = "";

                if (data.message) {
                    suggestionsDiv.innerHTML = `<p>${data.message}</p>`;
                    return;
                }

                data.forEach(employee => {
                    const resultItem = document.createElement("div");
                    resultItem.className = "result-item";
                    resultItem.innerHTML = `
                        <strong>${employee.name}</strong>
                        <span>${employee.company} | ${employee.title}</span>
                    `;

                    resultItem.addEventListener("click", function () {
                        fetchEmployeeDetails(employee.id);
                    });

                    suggestionsDiv.appendChild(resultItem);
                });
            })
            .catch(error => console.error("Error fetching search results:", error));
    }

    function fetchEmployeeDetails(employeeId) {
        fetch(`/employee/${employeeId}`)
            .then(response => response.json())
            .then(employee => {
                employeeDetailsDiv.innerHTML = `
                    <h2>${employee.name}</h2>
                    <p><strong>Company:</strong> ${employee.company}</p>
                    <p><strong>Position:</strong> ${employee.title}</p>
                `;
            })
            .catch(error => console.error("Error fetching employee details:", error));
    }
});
