import { getCookie } from './get-cookie.js'

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

        let key = (Object.keys(msg))[0];
        let message = msg[key][0]

        if (key === 'serial_number') {
            key = 'Serial Number'
        } else if (key === 'purchase_order_number') {
            key = 'PO number'
        } else if (key === 'domain') {
            key = 'Domain'
        } else if (key === 'ip_address') {
            key = 'IP Address'
        } else if (key === 'manufacturer') {
            key = 'Manufacturer'
        } else if (key === 'model') {
            key = 'Model'
        } else if (key === 'ip_address_sec') {
            key = 'IP Address Second'
        } else if (key === 'operating_system') {
            key = 'Operating System'
        } else if (key === 'building') {
            key = 'Building'
        } else if (key === 'business_processes_at_risk') {
            key = 'Process At Risk'
        } else if (key === 'support_model') {
            key = 'support_model'
        } else if (key === 'invoice_img') {
            key = 'Invoice image'
        } else if (key === 'owner_name') {
            key = 'Owner'
        } else {
            key = 'Device Name'
        }

        console.log(message)

        errorElement.textContent = `${key} - ${message}`;
        errorElement.classList.add('error-message');
        errorsContainer.appendChild(errorElement);
    });

    errorsContainer.style.display = 'block';
}

// Create
function submitDeviceForm() {
    event.preventDefault();

    const formData = new FormData(document.getElementById('deviceCreateForm'));
    const csrftoken = getCookie('csrftoken');
    const businessId = document.getElementById('businessId').value;
    formData.append('business', businessId);

    console.log(formData)

    fetch(createDeviceUrl, {
        method: 'POST',
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
            hideForm();
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
}

// Edit
function submitEditForm() {
    event.preventDefault(); // Prevent default form submission behavior

    const formData = new FormData(document.getElementById('deviceEditForm'));
    const csrftoken = getCookie('csrftoken');
    const deviceId = document.getElementById('editDeviceId').value;
    const editUrl = editDeviceUrl.replace("0", deviceId);

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
            hideForm();
            window.location.reload();
        })
        .catch(error => {
            console.log(error)
            if (typeof error === 'string' || typeof error === 'object') {
                // Handle non-JSON errors, potentially parsing for known error messages
                // For simplicity, showing the received error string directly
                displayErrors({ message: [error] }, 'errorsEditContainer');
            } else {
                console.error('Error:', error);
                displayErrors({ message: ["JS error"] }, 'errorsEditContainer');
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
            displayErrors({ message: [error.detail] }, 'errorsDeleteConfirmContainer');
        });
}

