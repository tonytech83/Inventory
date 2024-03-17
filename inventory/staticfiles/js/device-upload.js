function showUploadForm(businessId) {
    document.getElementById('uploadCSVForm').style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';

    const form = document.getElementById('uploadCSVForm');
}

function hideUploadForm() {
    document.getElementById('uploadCSVForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none'; // If you're using a backdrop
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

document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadCSVForm');
    const businessId = uploadForm.getAttribute('data-business-id');
    const uploadCsvUrl = `/business/${businessId}/upload-csv/`;

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
                console.log('Success:', data);
                displayImportResults(data.results); // Call function to display results
                hideUploadForm();
                // Consider if you really need to reload the page
                // window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});

function displayImportResults(results) {
    const resultsElement = document.getElementById('importResults');
    const resultsList = document.getElementById('importResultsList');
    resultsList.innerHTML = ''; // Clear previous results

    results.forEach(result => {
        const li = document.createElement('li');
        li.textContent = `${result.device_name}: ${result.status}`;
        if (result.status === 'error') {
            li.textContent += ` - Error: ${result.error}`;
            li.style.color = 'red';
        } else {
            li.style.color = 'green'; // Success color
        }
        resultsList.appendChild(li);
    });

    resultsElement.style.display = 'block'; // Show results
}

// document.addEventListener('DOMContentLoaded', function () {
//     const uploadForm = document.getElementById('uploadCSVForm');
//     const businessId = uploadForm.getAttribute('data-business-id');
//     const uploadCsvUrl = `/business/${businessId}/upload-csv/`;
//
//     uploadForm.addEventListener('submit', function (e) {
//         e.preventDefault();
//
//         const formData = new FormData(uploadForm);
//         const csrftoken = getCookie('csrftoken');
//
//         fetch(uploadCsvUrl, {
//             method: 'POST',
//             headers: {
//                 'X-CSRFToken': csrftoken,
//             },
//             body: formData,
//         })
//             .then(response => {
//                 if (response.ok) {
//                     return response.json();
//                 } else {
//                     throw new Error('Network response was not ok');
//                 }
//             })
//             .then(data => {
//                 console.log('Success:', data);
//                 hideUploadForm();
//                 window.location.reload();
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//             });
//     });
// });
