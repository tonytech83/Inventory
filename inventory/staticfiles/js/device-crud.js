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

    // console.log(deviceInvoiceImage)

    if (deviceInvoiceImage !== 'null') {
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

    document.getElementById('errorsEditContainer').style.display = 'none';
    document.getElementById('errorsContainer').style.display = 'none';
}

function hideDeleteForm() {
    document.getElementById('deleteDeviceForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';
}

function displayErrors(errors, containerId) {
    const errorsContainer = document.getElementById(containerId);
    errorsContainer.innerHTML = '';

    errors.message.forEach(msg => {
        const errorElement = document.createElement('p');
        errorElement.textContent = msg;
        errorElement.classList.add('error-message'); // Ensure you have CSS for this class
        errorsContainer.appendChild(errorElement);
    });

    errorsContainer.style.display = 'block';
}

// Create
function submitDeviceForm() {
    event.preventDefault(); // Prevent form from submitting the default way

    const formData = new FormData(document.getElementById('deviceCreateForm'));
    const csrftoken = getCookie('csrftoken');
    const businessId = document.getElementById('businessId').value;
    formData.append('business', businessId);

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
                // Read the response as text
                return response.text().then(html => {
                    // Define known error messages and their user-friendly equivalents
                    const errorMappings = {
                        '{"device_name":["This field may not be blank."]}': "The Hostname can not be blank.",
                        '{"detail":"UNIQUE constraint failed: devices_device.serial_number"}': "The Serial number is already used. Please use a unique Serial number.",
                        '{"device_name":["device with this device name already exists."]}': "The Hostname is already used. Please use a unique Hostname.",
                        '{"device_name":["Ensure this field has at least 2 characters."]}': "Ensure Hostname field has at least 2 characters."
                    };

                    let userFriendlyError = "An unexpected error occurred. Please try again.";
                    Object.keys(errorMappings).forEach(errorPattern => {
                        if (html.includes(errorPattern)) {
                            userFriendlyError = errorMappings[errorPattern];
                        }
                    });

                    // Reject the promise
                    return Promise.reject(userFriendlyError);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            hideForm();
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            displayErrors({message: [error]}, 'errorsContainer');
        });
}

// Edit
function submitEditForm() {
    event.preventDefault(); // Prevent default form submission behavior

    const formData = new FormData(document.getElementById('deviceEditForm'));
    const csrftoken = getCookie('csrftoken');
    const deviceId = document.getElementById('editDeviceId').value;
    const editUrl = editDeviceUrl.replace("0", deviceId); // Ensure you have defined editDeviceUrl

    const businessId = document.getElementById('businessId').value; // Ensure you have this element in your form
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
            const contentType = response.headers.get("Content-Type");
            if (!response.ok) {
                if (contentType && contentType.indexOf("application/json") !== -1) {
                    // Parse response as JSON
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
            hideForm();
            window.location.reload();
        })
        .catch(error => {
            // Determine error type (JSON or string)
            if (typeof error === 'object' && error.detail) {
                displayErrors({message: [error.detail]}, 'errorsEditContainer');
            } else if (typeof error === 'string') {
                // Handle non-JSON errors, potentially parsing for known error messages
                // For simplicity, showing the received error string directly
                displayErrors({message: [error]}, 'errorsEditContainer');
            } else {
                console.error('Error:', error);
                displayErrors({message: ["An unexpected error occurred. Please try again."]}, 'errorsEditContainer');
            }
        });
}

// Delete
function confirmDelete() {
    const deviceId = document.getElementById('deleteDeviceId').value;
    const deleteUrl = deleteDeviceUrl.replace("0", `${deviceId}`);

    const csrftoken = getCookie('csrftoken')

    fetch(deleteUrl, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json',
        },
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => Promise.reject(data));
            }
            hideDeleteForm();
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            displayErrors({message: [error.detail]}, 'errorsDeleteConfirmContainer');
        });
}

