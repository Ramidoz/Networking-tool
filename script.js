document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded Successfully! ✅");

    /** SEARCH FUNCTIONALITY **/
    const searchBtn = document.getElementById("search-btn");
    const resultsContainer = document.getElementById("results-container");

    // Add event listener to each input field for Enter key
    document.querySelectorAll("input").forEach(input => {
        input.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();  // Prevents form submission
                fetchResults();
            }
        });
    });

    if (searchBtn) {
        searchBtn.addEventListener("click", fetchResults);
    } else {
        console.warn("⚠️ Search button not found!");
    }

    function fetchResults() {
        console.log("Fetching search results...");

        const firstNameInput = document.getElementById("first-name");
        const lastNameInput = document.getElementById("last-name");
        const jobTitleInput = document.getElementById("job-title");
        const companyNameInput = document.getElementById("company-name");

        let queryParams = new URLSearchParams({
            first_name: firstNameInput.value.trim(),
            last_name: lastNameInput.value.trim(),
            title: jobTitleInput.value.trim(),
            company: companyNameInput.value.trim()
        });

        fetch(`/search?${queryParams.toString()}`)
            .then(res => res.json())
            .then(data => {
                console.log("Search Response:", data);
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

    /** FILE UPLOAD FUNCTIONALITY **/
    const uploadForm = document.getElementById("upload-form");
    const fileInput = document.getElementById("file-input");
    const uploadStatus = document.getElementById("upload-status");

    if (uploadForm && fileInput) {
        uploadForm.addEventListener("submit", function (event) {
            event.preventDefault();  // ⛔ Prevent Form Reload

            if (fileInput.files.length === 0) {
                uploadStatus.innerHTML = "<p style='color: red;'>⚠️ Please select a file before uploading.</p>";
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
                if (data.error) {
                    uploadStatus.innerHTML = `<p style='color: red;'>❌ ${data.error}</p>`;
                } else {
                    uploadStatus.innerHTML = `<p style='color: green;'>✅ ${data.message}</p>`;
                }
            })
            .catch(error => {
                console.error("Upload failed:", error);
                uploadStatus.innerHTML = `<p style='color: red;'>❌ Upload failed! Check console.</p>`;
            });
        });
    } else {
        console.warn("⚠️ Upload form or file input not found!");
    }
});
