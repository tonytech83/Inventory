document.addEventListener('DOMContentLoaded', function () {

    function showTable(tableIdSuffix) {
        const tableId = `table${tableIdSuffix}`;
        document.getElementById(tableId).style.display = 'block';
        document.querySelector('.backdrop').style.display = 'block';
    }

    window.showTable = showTable;

    function hideForm() {
        document.querySelectorAll('.dashboard-table').forEach(table => {
            table.style.display = 'none';
        });
        document.querySelector('.backdrop').style.display = 'none';
        window.location.reload();
    }

    window.hideForm = hideForm;
});

let slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
    showDivs(slideIndex += n);
}

function showDivs(n) {
    let i;
    let x = document.getElementsByClassName("mySlides");
    if (n > x.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = x.length
    }
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    x[slideIndex - 1].style.display = "block";
}