const suppliersDataElement = document.getElementById('data-suppliers');
const suppliersData = JSON.parse(suppliersDataElement.getAttribute('data-suppliers'));

document.addEventListener('DOMContentLoaded', function () {
    const selectElement = document.getElementById('deviceSupplier');

    suppliersData.forEach(supplier => {
        const option = document.createElement('option');
        option.value = supplier.id;
        option.text = supplier.name;
        selectElement.appendChild(option);
    });
});