document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('file-input');
    const uploadStatus = document.getElementById('upload-status');

    if (fileInput.files.length === 0) {
        uploadStatus.innerHTML = '<p class="error">Please select a file.</p>';
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    uploadStatus.innerHTML = '<p>Uploading...</p>';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            uploadStatus.innerHTML = `<p class="error">${data.error}</p>`;
        } else {
            uploadStatus.innerHTML = '<p class="success">Upload successful!</p>';
        }
    })
    .catch(error => {
        uploadStatus.innerHTML = '<p class="error">Error uploading file.</p>';
        console.error(error);
    });
});

const searchInput = document.getElementById('search-input');
const suggestionsDiv = document.getElementById('suggestions');
const employeeDetailsDiv = document.getElementById('employee-details');

let debounceTimer;

searchInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        const query = this.value;
        if (query.length >= 1) {
            suggestionsDiv.innerHTML = '<div class="loading">Loading...</div>';
            fetch(`/search?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsDiv.innerHTML = '';
                    if (data.length === 0) {
                        suggestionsDiv.innerHTML = '<div class="no-results">No results found</div>';
                    } else {
                        data.forEach(employee => {
                            const suggestion = document.createElement('div');
                            suggestion.className = 'suggestion-item';
                            suggestion.innerHTML = `
                                <div>
                                    <strong>${employee.name}</strong><br>
                                    ${employee.company}<br>
                                    ${employee.title}
                                </div>
                            `;
                            suggestion.addEventListener('click', () => showEmployeeDetails(employee.id));
                            suggestionsDiv.appendChild(suggestion);
                        });
                    }
                })
                .catch(error => {
                    suggestionsDiv.innerHTML = '<div class="error">Error fetching results</div>';
                    console.error('Error:', error);
                });
        } else {
            suggestionsDiv.innerHTML = '';
        }
    }, 300);
});

function showEmployeeDetails(employeeId) {
    employeeDetailsDiv.innerHTML = '<div class="loading">Loading employee details...</div>';
    fetch(`/employee/${employeeId}`)
        .then(response => response.json())
        .then(employee => {
            employeeDetailsDiv.innerHTML = `<h2>${employee.name}</h2><p><strong>Company:</strong> ${employee.company}</p><p><strong>Position:</strong> ${employee.title}</p>`;
        })
        .catch(error => {
            employeeDetailsDiv.innerHTML = '<div class="error">Error fetching employee details</div>';
            console.error(error);
        });
}
