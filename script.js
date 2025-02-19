document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded Successfully! ✅");

    const uploadForm = document.getElementById("upload-form");
    const fileInput = document.getElementById("file-input");
    const uploadStatus = document.getElementById("upload-status");

    if (!uploadForm || !fileInput) {
        console.error("Upload form or file input is missing!");
        return;
    }

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
});
