document.addEventListener("DOMContentLoaded", function () {
    // Ensure search button event only runs when it exists
    const searchBtn = document.getElementById("search-btn");
    if (searchBtn) {
        searchBtn.addEventListener("click", fetchResults);
    }

    function fetchResults() {
        const firstNameInput = document.getElementById("first-name");
        const lastNameInput = document.getElementById("last-name");
        const jobTitleInput = document.getElementById("job-title");
        const companyNameInput = document.getElementById("company-name");

        let queryParams = new URLSearchParams({
            first_name: firstNameInput ? firstNameInput.value.trim() : "",
            last_name: lastNameInput ? lastNameInput.value.trim() : "",
            title: jobTitleInput ? jobTitleInput.value.trim() : "",
            company: companyNameInput ? companyNameInput.value.trim() : ""
        });

        fetch(`/search?${queryParams.toString()}`)
            .then(res => res.json())
            .then(data => {
                const resultsContainer = document.getElementById("results-container");
                if (resultsContainer) {
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
                }
            })
            .catch(error => console.error("Error fetching search results:", error));
    }

    // Upload functionality
    const uploadBtn = document.getElementById("upload-btn");
    if (uploadBtn) {
        uploadBtn.addEventListener("click", function () {
            const fileInput = document.getElementById("file-input");
            if (!fileInput || fileInput.files.length === 0) {
                alert("Please select a file before uploading.");
                return;
            }

            let formData = new FormData();
            formData.append("file", fileInput.files[0]);

            fetch("/upload", {
                method: "POST",
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message || data.error);
                })
                .catch(error => console.error("Upload failed:", error));
        });
    }
});
