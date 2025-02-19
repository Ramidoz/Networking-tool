document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded Successfully!"); // Debugging message

    const searchBtn = document.getElementById("search-btn");
    if (searchBtn) {
        console.log("Search button found");
        searchBtn.addEventListener("click", fetchResults);
    } else {
        console.error("Search button NOT found!");
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
                console.log("Search results received:", data);
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
        console.log("Upload button found");
        uploadBtn.addEventListener("click", function () {
            console.log("Upload button clicked!");

            const fileInput = document.getElementById("file-input");
            if (!fileInput || fileInput.files.length === 0) {
                alert("Please select a file before uploading.");
                return;
            }

            let formData = new FormData();
            formData.append("file", fileInput.files[0]);

            console.log("Uploading file:", fileInput.files[0].name);

            fetch("/upload", {
                method: "POST",
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    console.log("Upload response:", data);
                    alert(data.message || data.error);
                })
                .catch(error => console.error("Upload failed:", error));
        });
    } else {
        console.error("Upload button NOT found!");
    }
});
