import { getCookie } from './get-cookie.js'

window.showCreateBusinessForm = showCreateBusinessForm;
window.showEditBusinessForm = showEditBusinessForm;
window.hideBusinessForm = hideBusinessForm;
window.hideBusinessCreateForm = hideBusinessCreateForm;

const urls = document.getElementById('devicesUrls');
const editBusinessUrl = urls.getAttribute('data-edit-business-url');
const createBusinessUrl = urls.getAttribute('data-create-business-url')

function showCreateBusinessForm() {
    const createForm = document.getElementById('createBusinessForm');
    createForm.style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';
}

function showEditBusinessForm(businessId, businessName, businessCountry, businessIsVisible) {
    // console.log('-----------------------------------')
    // console.log('ID: ', businessId)
    // console.log('Name: ', businessName)
    // console.log('Country: ', businessCountry)
    // console.log('Visible: ', businessIsVisible)
    // console.log('-----------------------------------')

    // Populate the form fields
    document.getElementById('editBusinessId').value = businessId;
    document.getElementById('editBusinessName').value = businessName;
    document.getElementById('editBusinessCountry').value = businessCountry;
    document.getElementById('editBusinessIsVisible').checked = businessIsVisible === 'True';

    // Show the form and the backdrop
    document.getElementById('businessEditFormContainer').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';
}

function hideBusinessForm() {
    document.getElementById('businessEditFormContainer').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';
}

function hideBusinessCreateForm() {
    document.getElementById('createBusinessForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';
}

function displayErrors(errors, containerId) {
    const errorsContainer = document.getElementById(containerId);
    errorsContainer.innerHTML = '';

    errors.message.forEach(msg => {
        const errorElement = document.createElement('p');

        let key = (Object.keys(msg))[0];
        let message = msg[key][0]

        if (key === 'business_name') {
            key = 'Business name'
        } else {
            key = 'Country'
        }

        console.log(message)

        errorElement.textContent = `${key} - ${message}`;
        errorElement.classList.add('error-message');
        errorsContainer.appendChild(errorElement);
    });

    errorsContainer.style.display = 'block';
}

// Create
document.addEventListener('DOMContentLoaded', function () {
    const createForm = document.getElementById('BusinessCreateForm');
    if (createForm) {
        createForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const businessFormContainer = document.getElementById('businessFormContainer');
            // const createUrl = businessFormContainer.getAttribute('data-create-url');
            const createUrl = createBusinessUrl;

            const formData = new FormData(createForm);
            const csrftoken = getCookie('csrftoken');

            fetch(createUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                body: formData,
            })
                .then(response => {
                    const contentType = response.headers.get("Content-Type");
                    if (!response.ok) {
                        if (contentType && contentType.indexOf("application/json") !== -1) {
                            // Parse response to JSON
                            return response.json().then(data => Promise.reject(data));
                        } else {
                            // Non-JSON response, treat as text
                            return response.text().then(text => Promise.reject(text));
                        }
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Success:', data);
                    hideBusinessCreateForm();
                    window.location.reload();
                })
                .catch(error => {
                    if (typeof error === 'string' || typeof error === 'object') {
                        displayErrors({ message: [error] }, 'errorsContainer');
                    } else {
                        console.error('Error:', error);
                        displayErrors({ message: ["JS error"] }, 'errorsContainer');
                    }
                });
        });
    }
});

// Edit
document.addEventListener('DOMContentLoaded', function () {
    const editForm = document.getElementById('businessEditForm');

    if (editForm) {
        editForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const businessId = document.getElementById('editBusinessId').value;
            const formData = new FormData(editForm);
            const csrftoken = getCookie('csrftoken');

            const editUrl = editBusinessUrl.replace("0", `${businessId}`);
            console.log(editUrl);

            fetch(editUrl, {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(Object.fromEntries(formData))
            })
                .then(response => {
                    const contentType = response.headers.get("Content-Type");
                    if (!response.ok) {
                        if (contentType && contentType.indexOf("application/json") !== -1) {
                            // Parse response to JSON
                            return response.json().then(data => Promise.reject(data));
                        } else {
                            // Non-JSON response, treat as text
                            return response.text().then(text => Promise.reject(text));
                        }
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Success:', data);
                    hideBusinessForm();
                    window.location.reload();
                })
                .catch(error => {
                    if (typeof error === 'string' || typeof error === 'object') {
                        displayErrors({ message: [error] }, 'errorsEditBusinessContainer');
                    } else {
                        console.error('Error:', error);
                        displayErrors({ message: ["JS error"] }, 'errorsEditBusinessContainer');
                    }
                });
        });
    }
});
