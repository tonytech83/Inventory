import {getCookie} from './get-cookie.js'

window.showCreateForm = showCreateForm;
window.showEditForm = showEditForm;
window.showDeleteForm = showDeleteForm;
window.hideForm = hideForm;
window.confirmDelete = confirmDelete;
window.hideDeleteForm = hideDeleteForm;

const urls = document.getElementById('supplierUrls');
const createSupplierUrl = urls.getAttribute('data-create-supplier-url');
const editSupplierUrlTemplate = urls.getAttribute('data-edit-supplier-url');
const deleteSupplierUrlTemplate = urls.getAttribute('data-delete-supplier-url');

function showCreateForm() {
    // Show the form and the backdrop
    document.getElementById('createSupplierForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';
}

function showEditForm(supplierId, supplierName, supplierContactName, supplierCountryName, supplierPhoneNumber, supplierEmail) {
    // Populate the form fields
    document.getElementById('supplierId').value = supplierId;
    document.getElementById('supplierName').value = supplierName;
    document.getElementById('supplierContactName').value = supplierContactName;
    document.getElementById('supplierCountryName').value = supplierCountryName;
    document.getElementById('supplierPhoneNumber').value = supplierPhoneNumber;
    document.getElementById('supplierEmail').value = supplierEmail;

    // Show the form and the backdrop
    document.getElementById('editSupplierForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';
}

function showDeleteForm(supplierId, supplierName) {
    document.getElementById('deleteSupplierId').value = supplierId;
    document.getElementById('deleteSupplierName').innerText = supplierName;

    // Show the form and the backdrop
    document.getElementById('deleteSupplierForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block'

    // Hide the edit form if it's shown
    document.getElementById('editSupplierForm').style.display = 'none'
}

function hideForm() {
    // Hide the form and the backdrop
    document.getElementById('editSupplierForm').style.display = 'none';
    document.getElementById('createSupplierForm').style.display = 'none';
    document.getElementById('deleteSupplierForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';

    document.getElementById('errorsSupplierContainer').style.display = 'none';
    document.getElementById('errorsSupplierEditContainer').style.display = 'none';
}

function hideDeleteForm() {
    // Hide the delete form and backdrop
    document.getElementById('deleteSupplierForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';
}

function displayErrors(errors, containerId) {
    const errorsContainer = document.getElementById(containerId);
    if (!errorsContainer) {
        console.error('Error container not found:', containerId);
        return;
    }

    errorsContainer.innerHTML = '';

    // Iterate over each error
    Object.keys(errors).forEach(key => {
        errors[key].forEach(msg => {
            const errorElement = document.createElement('p');
            if (`${key}` === 'name') {
                errorElement.textContent = `Supplier name: ${msg}`;
            } else if (`${key}` === 'contact_name') {
                errorElement.textContent = `Contact name: ${msg}`;
            } else if (`${key}` === 'phone_number') {
                errorElement.textContent = `Phone number: ${msg}`;
            } else {
                errorElement.textContent = `Email: ${msg}`;
            }
            // errorElement.textContent = `${key}: ${msg}`;
            errorElement.classList.add('error-message');
            errorsContainer.appendChild(errorElement);
        });
    });

    errorsContainer.style.display = 'block';
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
            // displayErrors({message: [error]}, 'errorsSupplierContainer');
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
                return response.json();
            }
        }).then(data => {
            if (data) {
                displayErrors(data, 'errorsSupplierContainer');
            }
        }).catch(error => {
            console.error('Error:', error);
            displayErrors({message: ["An unexpected error occurred. Please try again."]}, 'errorsSupplierContainer');
        });
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
        const supplierCountryName = document.getElementById('supplierCountryName').value;
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
                supplier_country: supplierCountryName,
                phone_number: supplierPhoneNumber,
                email: supplierEmail
            }),
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (response.ok) {
                hideForm();
                window.location.reload();
            } else {
                console.error('Failed to edit supplier.');
                return response.json();
            }
        }).then(data => {
            if (data) {
                displayErrors(data, 'errorsSupplierEditContainer');
            }
        }).catch(error => {
            console.error('Error:', error);
            displayErrors({message: ["An unexpected error occurred. Please try again."]}, 'errorsSupplierEditContainer');
        });
    });
});

// Cards view
document.addEventListener('DOMContentLoaded', function () {
    const suppliersDataElement = document.getElementById('data-container');
    const suppliersData = JSON.parse(suppliersDataElement.getAttribute('data-suppliers'));

    console.log(suppliersData)

    let cardsContainer = $('<div class="cards-container"></div>');

    suppliersData.forEach(function (supplier) {
        let card = $('<div class="supplier-card"></div>');
        card.append('<h5 class="card-title">' + supplier.name + '</h5>');
        card.append('<p>Contact: ' + supplier.contact_name + '</p>');
        card.append('<p>Country: ' + supplier.supplier_country + '</p>');
        card.append('<p>Phone: ' + supplier.phone_number + '</p>');
        card.append('<p>Email: <a href="mailto:' + supplier.email + '">' + supplier.email + '</a></p>');

        card.on('click', function () {
            showEditForm(supplier.id, supplier.name, supplier.contact_name, supplier.supplier_country, supplier.phone_number, supplier.email);
        });

        cardsContainer.append(card);
    });

    $('#data-container-no-handsontable').append(cardsContainer);

});

// Toggle between Handsontable and Cards
$(function () {
    $('#handsontable-view').hide();

    $('#toggle-view-btn').click(function () {
        // Toggle visibility of each view
        $('#handsontable-view').toggle();
        $('#cards-view').toggle();
    });
});