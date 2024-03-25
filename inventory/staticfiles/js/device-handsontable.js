document.addEventListener('DOMContentLoaded', function () {
    const devicesDataElement = document.getElementById('data-container');
    const devicesData = JSON.parse(devicesDataElement.getAttribute('data-devices'))

    const data = devicesData.map(function (item) {
        return [
            item.device_name,
            item.domain,
            item.description,
            item.status,
            item.manufactur,
            item.model,
            item.ip_address,
            item.ip_address_sec,
            item.operating_system,
            item.building,
            item.category,
            item.sub_category,
            item.serial_number,
            item.owner_name,
            // Support
            item.support_model,
            item.purchase_order_number,
            item.invoice_img,
            item.sos,
            item.eos,
            item.eol,
            // Risk
            item.business_processes_at_risk,
            item.impact,
            item.likelihood,
            // Supplier
            item.supplier_name,
        ];
    });

    const container = document.getElementById('data-container');

    const hot = new Handsontable(container, {
        data: data,
        columns: [
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
            {type: 'text'},
        ],

        <!-- Start General settings -->
        width: '100%', // size of the table
        stretchH: 'all', // stretch horizontally table
        height: '64vh',
        overflow: 'hidden',
        <!-- End General settings -->

        <!-- Start Columns settings -->
        columnSorting: true,
        colHeaders: ['Hostname', 'Domain', 'Description', 'Status', 'Manufacturer', 'Model', 'IP Address', 'IP Address Second', 'Operating System', 'Building', 'Category', 'Sub Category', 'Serial Number', 'Owner', 'Support Model', 'PO Number', 'Invoice', 'SOS', 'EOS', 'EOL', 'Process at risk', 'Impact', 'Likelihood', 'Supplier'],
        hiddenColumns: {
            columns: [1, 2, 4, 6, 7, 8, 9, 14, 15, 16, 17, 19, 20, 21, 22],
            indicators: false
        },
        // Make first column link to edit
        afterRenderer: function (TD, row, col, prop, value, cellProperties) {
            if (col === 0) {
                TD.innerHTML = `<span onclick="showDeviceEditForm(
                            ${devicesData[row].id},
                            '${devicesData[row].device_name}',
                            '${devicesData[row].domain}',
                            '${devicesData[row].description}',
                            '${devicesData[row].status}',
                            '${devicesData[row].manufacturer}',
                            '${devicesData[row].model}',
                            '${devicesData[row].ip_address}',
                            '${devicesData[row].ip_address_sec}',
                            '${devicesData[row].operating_system}',
                            '${devicesData[row].building}',
                            '${devicesData[row].category}',
                            '${devicesData[row].sub_category}',
                            '${devicesData[row].serial_number}',
                            '${devicesData[row].owner_name}',
                            // Support
                            '${devicesData[row].support_model}',
                            '${devicesData[row].purchase_order_number}',
                            '${devicesData[row].invoice_img}',
                            '${devicesData[row].sos}',
                            '${devicesData[row].eos}',
                            '${devicesData[row].eol}',
                            // Risk
                            '${devicesData[row].business_processes_at_risk}',
                            '${devicesData[row].impact}',
                            '${devicesData[row].likelihood}',
                            // Supplier
                            '${devicesData[row].supplier_name}',
                            )">${value}</span>`;
            }
        },
        colWidths: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        <!-- End Columns settings -->

        <!-- Start Rows settings -->
        rowHeaders: false,
        <!-- End Rows settings -->

        <!-- Start Filters settings -->
        filters: true,
        dropdownMenu: ['filter_by_value', 'filter_action_bar'],
        // Remove all selections in dropdownMenu
        // afterDropdownMenuShow(instance) {
        //     var filters = instance.hot.getPlugin('filters');
        //     console.log(filters.components.get('filter_by_value').elements[0])
        //     filters.components.get('filter_by_value').elements[0].onClearAllClick({
        //         preventDefault: function () {
        //         }
        //     });
        // },

        // Disable cell selection
        disableVisualSelection: true,
        <!-- End Filters settings -->

        <!-- Start Other settings -->
        readOnly: true,
        licenseKey: 'non-commercial-and-evaluation',
        <!-- End Other settings -->
    });

    // // Start part of the `Remove all selection in dropdown menu`
    // var filters = hot.getPlugin('filters');
    //
    // window.hot = hot;
    // window.filters = filters;
    //
    // hot.render();
    // // End part of the `Remove all selection`

    // Download data to CSV
    const button = document.querySelector('#export-file');
    const exportPlugin = hot.getPlugin('exportFile');

    button.addEventListener('click', () => {
        exportPlugin.downloadFile('csv', {
            bom: false,
            columnDelimiter: ',',
            columnHeaders: true,
            exportHiddenColumns: true,
            exportHiddenRows: true,
            fileExtension: 'csv',
            filename: 'devices_[YYYY]-[MM]-[DD]',
            mimeType: 'text/csv',
            rowDelimiter: '\r\n',
            rowHeaders: false,
            // range: [0, 0, devicesData.length, 10] //
        });
    });
});