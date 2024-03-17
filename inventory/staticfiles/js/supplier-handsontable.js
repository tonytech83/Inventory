document.addEventListener('DOMContentLoaded', function () {
    const suppliersDataElement = document.getElementById('data-container');
    const suppliersData = JSON.parse(suppliersDataElement.getAttribute('data-suppliers'));

    const data = suppliersData.map(function (item) {
        return [
            item.name,
            item.contact_name,
            item.phone_number,
            item.email,
        ];
    });

    const container = document.getElementById('data-container');
    const button = document.querySelector('#export-file');
    // button for downloading
    const hot = new Handsontable(container, {
            data: data,
            columns: [
                {data: 0, renderer: "html"},  // Ensure the first column renders HTML for the link
                {},
                {},
                {},

            ],

            <!-- Start General settings -->
            width: '100%', // size of the table
            // customBorders: true,
            stretchH: 'all', // stretch horizontally table
            <!-- End General settings -->

            <!-- Start Columns settings -->
            columnSorting: true,
            colHeaders: ['Name', 'Contact name', 'Phone number', 'Email'],
            // Make first column link to edit
            afterRenderer: function (TD, row, col, prop, value, cellProperties) {
                if (col === 0) {
                    TD.innerHTML = `<span onclick="showEditForm(
                            ${suppliersData[row].id},
                             '${suppliersData[row].name}',
                              '${suppliersData[row].contact_name}',
                               '${suppliersData[row].phone_number}',
                                '${suppliersData[row].email}'
                                )">${value}</span>`;
                }
            },
            <!-- End Columns settings -->

            <!-- Start Rows settings -->
            rowHeaders: false,
            <!-- End Rows settings -->

            <!-- Start Filters settings -->
            filters:
                true,
            // dropdownMenu: true,
            dropdownMenu: ['filter_by_value', 'filter_action_bar'],
            // Disable cell selection
            disableVisualSelection: true,
            <!-- End Filters settings -->

            <!-- Start Other settings -->
            readOnly:
                true,
            licenseKey:
                'non-commercial-and-evaluation',
            <!-- End Other settings -->
        })
    ;

    // Download data to CSV
    const exportPlugin = hot.getPlugin('exportFile');

    button.addEventListener('click', () => {
        exportPlugin.downloadFile('csv', {
            bom: false,
            columnDelimiter: ',',
            columnHeaders: true,
            exportHiddenColumns: true,
            exportHiddenRows: true,
            fileExtension: 'csv',
            filename: 'suppliers_[YYYY]-[MM]-[DD]',
            mimeType: 'text/csv',
            rowDelimiter: '\r\n',
            rowHeaders: false,
        });
    });

});