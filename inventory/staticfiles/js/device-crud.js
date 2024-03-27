import {getCookie} from './get-cookie.js'

window.showCreateForm = showCreateForm;
window.showDeviceEditForm = showDeviceEditForm;
window.showDeleteForm = showDeleteForm;
window.submitDeviceForm = submitDeviceForm;
window.submitEditForm = submitEditForm;
window.hideForm = hideForm;
window.hideDeleteForm = hideDeleteForm;
window.confirmDelete = confirmDelete;

const urls = document.getElementById('devicesUrls');
const createDeviceUrl = urls.getAttribute('data-create-device-url')
const editDeviceUrl = urls.getAttribute('data-edit-device-url');
const deleteDeviceUrl = urls.getAttribute('data-delete-device-url');


function showCreateForm() {
    // Show the form and the backdrop
    document.getElementById('createForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';
}

function showDeviceEditForm(deviceId, deviceHostName, deviceDomain, deviceDescription, deviceStatus, deviceManufacturer, deviceModel, deviceIpAddress, deviceIpAddressSecondary, deviceOperatingSystem, deviceBuilding, deviceCategory, deviceSubCategory, deviceSerialNumber, deviceOwnerName, deviceSupportModel, devicePurchaseOrderNumber, deviceInvoiceImage, deviceStartOfSupport, deviceEndOfSupport, deviceEndOfLife, deviceBusinessProcessAtRisk, deviceImpact, deviceLikelihood) {
    document.getElementById('editDeviceId').value = deviceId;
    document.getElementById('editDeviceHostName').value = deviceHostName;
    document.getElementById('editDeviceDomain').value = deviceDomain !== 'null' ? deviceDomain : '';
    document.getElementById('editDeviceDescription').value = deviceDescription !== 'null' ? deviceDescription : '';
    document.getElementById('editDeviceStatus').value = deviceStatus;
    document.getElementById('editDeviceManufacturer').value = deviceManufacturer !== 'null' ? deviceManufacturer : '';
    document.getElementById('editDeviceModel').value = deviceModel !== 'null' ? deviceModel : '';
    document.getElementById('editDeviceIpAddress').value = deviceIpAddress !== 'null' ? deviceIpAddress : '';
    document.getElementById('editDeviceIpAddressSecondary').value = deviceIpAddressSecondary !== 'null' ? deviceIpAddressSecondary : '';
    document.getElementById('editDeviceOperatingSystem').value = deviceOperatingSystem !== 'null' ? deviceOperatingSystem : '';
    document.getElementById('editDeviceBuilding').value = deviceBuilding !== 'null' ? deviceBuilding : '';
    document.getElementById('editDeviceCategory').value = deviceCategory;
    document.getElementById('editDeviceSubCategory').value = deviceSubCategory;
    document.getElementById('editDeviceSerialNumber').value = deviceSerialNumber !== 'null' ? deviceSerialNumber : '';
    document.getElementById('editDeviceOwnerName').value = deviceOwnerName !== 'null' ? deviceOwnerName : '';
    // Support
    document.getElementById('editDeviceSupportModel').value = deviceSupportModel !== 'null' ? deviceSupportModel : '';
    document.getElementById('editDevicePurchaseOrderNumber').value = devicePurchaseOrderNumber !== 'null' ? devicePurchaseOrderNumber : '';

    // Check if there's an invoice URL and set up a download link
    const invoiceLinkElement = document.getElementById('existingInvoiceLink');

    if (deviceInvoiceImage) {
        const fullPath = deviceInvoiceImage.startsWith('/media/') ? deviceInvoiceImage : `/media/${deviceInvoiceImage}`;
        invoiceLinkElement.setAttribute('href', fullPath);
        invoiceLinkElement.style.display = 'inline';
    } else {
        invoiceLinkElement.style.display = 'none';
    }
    document.getElementById('editDeviceStartOfSupport').value = deviceStartOfSupport;
    document.getElementById('editDeviceEndOfSupport').value = deviceEndOfSupport;
    document.getElementById('editDeviceEndOfLife').value = deviceEndOfLife;
    document.getElementById('editDeviceBusinessProcessAtRisk').value = deviceBusinessProcessAtRisk !== 'null' ? deviceBusinessProcessAtRisk : '';
    document.getElementById('editDeviceImpact').value = deviceImpact;
    document.getElementById('editDeviceLikelihood').value = deviceLikelihood;

    // Show the Host name of the current device instead of 'Edit Device'
    document.querySelector('.action-title').textContent = '-- ' + deviceHostName + ' --';

    document.getElementById('editForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';
}

function showDeleteForm(deviceId, deviceHostName) {
    document.getElementById('deleteDeviceId').value = deviceId;
    document.getElementById('deleteDeviceHostName').innerText = deviceHostName;


    // Show the form and the backdrop
    document.getElementById('deleteDeviceForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block'

    // Hide the edit form if it's shown
    document.getElementById('editForm').style.display = 'none'
}

function hideForm() {
    document.getElementById('createForm').style.display = 'none';
    document.getElementById('editForm').style.display = 'none';
    document.getElementById('deleteDeviceForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';
}

function hideDeleteForm() {
    // Hide the delete form and backdrop
    document.getElementById('deleteDeviceForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';
}

// Create
function submitDeviceForm() {
    event.preventDefault(); // Add this if submitDeviceForm is called on form submit

    const formData = new FormData(document.getElementById('deviceCreateForm'));
    const csrftoken = getCookie('csrftoken');
    const businessId = document.getElementById('businessId').value;
    formData.append('business', businessId);

    // const createDeviceUrl = document.getElementById('devicesUrls').getAttribute('data-create-device-url'); // Ensure this is correct

    fetch(createDeviceUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
        },
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            hideForm();
            window.location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle errors (e.g., showing an error message)
        });
}

// Edit
function submitEditForm() {
    event.preventDefault(); // Prevent default form submission behavior

    const formData = new FormData(document.getElementById('deviceEditForm'));
    const csrftoken = getCookie('csrftoken')
    const deviceId = document.getElementById('editDeviceId').value;
    const editUrl = editDeviceUrl.replace("0", `${deviceId}`)

    // const editDeviceUrl = document.getElementById('devicesUrls').getAttribute('data-edit-device-url').replace('0', deviceId);


    const businessId = document.getElementById('businessId').value;
    formData.append('business', businessId);

    fetch(editUrl, {
        method: 'PATCH',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
        },
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            hideForm(); // Hide the edit form
            window.location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// Delete
function confirmDelete() {
    // Get the device ID and create deleteUrl
    const deviceId = document.getElementById('deleteDeviceId').value;
    const deleteUrl = deleteDeviceUrl.replace("0", `${deviceId}`);

    console.log(deleteUrl)

    const csrftoken = getCookie('csrftoken')

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

