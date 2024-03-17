function showCreateBusinessForm() {
    const createForm = document.getElementById('createForm');
    createForm.style.display = 'block';
    document.querySelector('.backdrop').style.display = 'block';
}

function hideForm() {
    document.getElementById('createForm').style.display = 'none';
    document.querySelector('.backdrop').style.display = 'none';
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
    const createForm = document.getElementById('BusinessCreateForm');

    createForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(createForm);
        const csrftoken = getCookie('csrftoken');

        const createBusinessUrl = '{% url "create-business" %}';

        fetch(createBusinessUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                hideForm();
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});