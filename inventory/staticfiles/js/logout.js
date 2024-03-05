document.addEventListener('DOMContentLoaded', function () {
    const logoutLink = document.querySelector('#logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function (e) {
            e.preventDefault();
            const logoutUrl = document.querySelector('#logout-config').getAttribute('data-logout-url');
            fetch(logoutUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Ensure you have a function to get CSRF token from cookies
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                },
                credentials: 'same-origin'
            }).then(response => {
                if (response.ok) {
                    window.location.href = "/"; // Redirect to home or any other page
                }
            }).catch(error => console.error('Error:', error));
        });
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
});