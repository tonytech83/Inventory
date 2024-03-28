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

