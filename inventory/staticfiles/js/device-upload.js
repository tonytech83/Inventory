function showUploadForm(businessId) {
    document.getElementById('uploadCSVForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';

    const form = document.getElementById('uploadCSVForm');
}

function hideUploadForm() {
    document.getElementById('uploadCSVForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none'; // If you're using a backdrop

    // Buttons
    const inputFieldId = document.getElementById('inputFieldId')
    const uploadButton = document.getElementById('upload-button')
    const cancelButton = document.getElementById('cancel-button')
    const closeButton = document.getElementById('close-button')
    inputFieldId.value = ''
    uploadButton.style.visibility = 'visible';
    cancelButton.style.visibility = 'visible';
    closeButton.style.display = 'none';


    const resultsList = document.getElementById('importResultsList');
    resultsList.innerHTML = '';
    window.location.reload();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function displayImportResults(results) {
    const resultsElement = document.getElementById('importResults');
    const resultsList = document.getElementById('importResultsList');
    resultsList.innerHTML = ''; // Clear previous results

    results.forEach(results => {
        const li = document.createElement('li');
        li.textContent = `${results.device_name}: ${results.status}`;
        if (results.status === 'Error') {
            let message = '';
            if (results.error.includes("UNIQUE constraint failed: devices_device.device_name")) {
                message = "The device name should be unique."
            }
            li.textContent += ` - Message: ${message}`;
            li.style.color = 'red';
        } else {
            li.style.color = 'green'; // Success color
        }
        resultsList.appendChild(li);
    });

    resultsElement.style.display = 'block'; // Show results
}

document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadCSVForm');
    const businessId = uploadForm.getAttribute('data-business-id');
    const uploadCsvUrl = `/business/${businessId}/upload-csv/`;

    // Buttons
    const uploadButton = document.getElementById('upload-button')
    const cancelButton = document.getElementById('cancel-button')
    const closeButton = document.getElementById('close-button')

    uploadForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(uploadForm);
        const csrftoken = getCookie('csrftoken');

        fetch(uploadCsvUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                // console.log('Success:', data);
                displayImportResults(data.results); // Call function to display results

                uploadButton.style.visibility = 'hidden';
                cancelButton.style.visibility = 'hidden';
                closeButton.style.display = 'inline-block';
                // hideUploadForm();
                // Consider if you really need to reload the page
                // window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});



