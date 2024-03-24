import {getCookie} from './get-cookie.js'

window.showCreateBusinessForm = showCreateBusinessForm;
window.showEditBusinessForm = showEditBusinessForm;
window.hideBusinessForm = hideBusinessForm;

const urls = document.getElementById('devicesUrls');
const editBusinessUrl = urls.getAttribute('data-edit-business-url');

function showCreateBusinessForm() {
    const createForm = document.getElementById('createForm');
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

// Create
document.addEventListener('DOMContentLoaded', function () {
    const createForm = document.getElementById('BusinessCreateForm');
    if (createForm) {
        createForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const businessFormContainer = document.getElementById('businessFormContainer');
            const createUrl = businessFormContainer.getAttribute('data-create-url');

            const formData = new FormData(createForm);
            const csrftoken = getCookie('csrftoken');

            fetch(createUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    window.location.reload();
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Error handling logic here
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
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Success:', data);
                    document.getElementById('businessEditFormContainer').style.display = 'none';
                    window.location.reload();
                })
                .catch((error) => {
                    console.error('Error:', error);

                });
        });
    }
});
