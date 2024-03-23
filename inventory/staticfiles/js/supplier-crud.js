import {getCookie} from './get-cookie.js'

window.showCreateForm = showCreateForm;
window.showEditForm = showEditForm;
window.showDeleteForm = showDeleteForm;
window.hideForm =hideForm;
window.confirmDelete = confirmDelete;
window.hideDeleteForm = hideDeleteForm;

const urls = document.getElementById('supplierUrls');
const createSupplierUrl = urls.getAttribute('data-create-supplier-url');
const editSupplierUrlTemplate = urls.getAttribute('data-edit-supplier-url');
const deleteSupplierUrlTemplate = urls.getAttribute('data-delete-supplier-url');

function showCreateForm() {
    // Show the form and the backdrop
    document.getElementById('createForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';
}

function showEditForm(supplierId, supplierName, supplierContactName, supplierPhoneNumber, supplierEmail) {
    // Populate the form fields
    document.getElementById('supplierId').value = supplierId;
    document.getElementById('supplierName').value = supplierName;
    document.getElementById('supplierContactName').value = supplierContactName;
    document.getElementById('supplierPhoneNumber').value = supplierPhoneNumber;
    document.getElementById('supplierEmail').value = supplierEmail;

    // Show the form and the backdrop
    document.getElementById('editForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';
}

function showDeleteForm(supplierId, supplierName) {
    document.getElementById('deleteSupplierId').value = supplierId;
    document.getElementById('deleteSupplierName').innerText = supplierName;

    // Show the form and the backdrop
    document.getElementById('deleteForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block'

    // Hide the edit form if it's shown
    document.getElementById('editForm').style.display = 'none'
}

function hideForm() {
    // Hide the form and the backdrop
    document.getElementById('editForm').style.display = 'none';
    document.getElementById('createForm').style.display = 'none';
    document.getElementById('deleteForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';
}

function hideDeleteForm() {
    // Hide the delete form and backdrop
    document.getElementById('deleteForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';
}

function confirmDelete() {
    // Get the supplier ID
    const supplierId = document.getElementById('deleteSupplierId').value;

    const deleteUrl = deleteSupplierUrlTemplate.replace("0", `${supplierId}`);

    const csrftoken = getCookie('csrftoken');

    fetch(deleteUrl, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            hideDeleteForm();
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });

}

// Create
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("supplierCreateForm").addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());


        const csrftoken = getCookie('csrftoken');

        fetch(createSupplierUrl, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (response.ok) {
                hideForm();
                window.location.reload();
            } else {
                console.error('Failed to create supplier.');
            }
        }).catch(error => console.error('Error:', error));
    });

});

// Edit
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("supplierEditForm").addEventListener("submit", function (e) {
        e.preventDefault();

        // Retrieves the supplier ID
        const supplierId = document.getElementById('supplierId').value;

        const editUrl = editSupplierUrlTemplate.replace("0", `${supplierId}`);

        // Prepare the request payload
        const supplierName = document.getElementById('supplierName').value;
        const supplierContactName = document.getElementById('supplierContactName').value;
        const supplierPhoneNumber = document.getElementById('supplierPhoneNumber').value;
        const supplierEmail = document.getElementById('supplierEmail').value;

        // Retrieve CSRF token
        const csrftoken = getCookie('csrftoken');

        // Make the fetch request
        fetch(editUrl, {
            method: 'PATCH',
            body: JSON.stringify({
                name: supplierName,
                contact_name: supplierContactName,
                phone_number: supplierPhoneNumber,
                email: supplierEmail
            }),
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                if (response.ok) {
                    hideForm();
                    window.location.reload();
                } else {
                    console.error('Failed to edit supplier.');
                }
            })
            .catch(error => console.error('Error:', error));
    });
});
