import {getCookie} from './get-cookie.js'

window.showUploadForm = showUploadForm;
window.hideUploadForm = hideUploadForm;
window.displayImportResults = displayImportResults;

function showUploadForm(businessId) {
    document.getElementById('uploadCSVForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';

    const form = document.getElementById('uploadCSVForm');
}

function hideUploadForm() {
    document.getElementById('uploadCSVForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';

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

function displayImportResults(results) {
    const resultsElement = document.getElementById('importResults');
    const resultsList = document.getElementById('importResultsList');
    resultsList.innerHTML = '';

    results.forEach(results => {
        const li = document.createElement('li');
        li.textContent = `${results.device_name}: ${results.status}`;

        if (results.status === 'Error') {
            console.log(results.error)
            let message = '';
            if (results.error.includes("UNIQUE constraint failed: devices_device.device_name")) {
                message = "The device name should be unique."
            } else if (results.error.includes("UNIQUE constraint failed: devices_device.serial_number")) {
                message = "The serial number of device should be unique."
            } else if (results.device_name === null) {
                message = 'Please provide name of the device.'
            } else if (results.error.includes("NOT NULL constraint failed: devices_device.model")) {
                message = 'Device model can be empty.'
            }
            li.textContent += ` - Message: ${message}`;
            li.style.color = 'red';
        } else {
            li.style.color = 'green';
        }
        resultsList.appendChild(li);
    });

    // Show results
    resultsElement.style.display = 'block';
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

        const fileInput = document.getElementById('inputFieldId');
        const uploadMessage = document.getElementById('uploadMessage');
        const uploadDescription = document.getElementById('uploadDescription');

        // Check if a file has been selected
        if (!fileInput.files.length) {
            uploadDescription.style.display = 'none';
            uploadMessage.style.display = 'block';
            return;
        } else {
            uploadMessage.style.display = 'none';
            uploadDescription.style.display = 'none';
        }

        // Continue if a file is selected
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
                displayImportResults(data.results);

                // const uploadDescription = document.getElementById('uploadDescription');
                // uploadDescription.style.display = 'none';

                uploadButton.style.visibility = 'hidden';
                cancelButton.style.visibility = 'hidden';
                closeButton.style.display = 'inline-block';

            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});

