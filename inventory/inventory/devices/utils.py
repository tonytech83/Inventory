import random
from datetime import date
from inventory.devices.models import Device


def create_devices_form_upload(sheet, business):
    """
    Processes an Excel sheet to bulk create device entries associated with a given business in the database.

    Parameters:
        sheet (openpyxl.worksheet.worksheet.Worksheet): The worksheet object from which device data is read.
        business (Business): The business instance to which these devices will be associated.

    Returns:
        list of dict: A list containing the results for each device processing attempt, including the device name and
                      the status ('success' or 'Error' with an error message if applicable).

    Each Device creation failure due to data issues is caught and returned with an error message, allowing the caller
    to identify and address these issues in the dataset.
    """

    results = []

    for row in sheet.iter_rows(min_row=3):
        # Random 4 digits if no serial number in file
        four_random_digits = ''.join(str(random.randint(0, 9)) for _ in range(4))

        try:
            Device.objects.create(
                device_name=row[0].value,
                domain=row[1].value,
                description=row[2].value,
                status=row[3].value,
                category=row[4].value,
                sub_category=row[5].value,
                manufacturer=row[6].value,
                model=row[7].value,
                ip_address=row[8].value,
                ip_address_sec=row[9].value,
                serial_number=row[10].value if row[10].value else f'{row[0].value}-{four_random_digits}',
                operating_system=row[11].value,
                building=row[12].value,
                owner_name=row[13].value,
                support_model=row[14].value,
                purchase_order_number=row[15].value,
                sos=row[17].value if row[17].value else date.today(),
                eos=row[18].value if row[18].value else date.today(),
                eol=row[19].value if row[19].value else date.today(),
                business_processes_at_risk=row[20].value,
                impact=row[21].value if row[21].value else 1,
                likelihood=row[22].value if row[22].value else 1,
                business=business,
            )
            results.append({'device_name': row[0].value, 'status': 'success'})
        except Exception as e:
            results.append({'device_name': row[0].value, 'status': 'Error', 'error': str(e)})
            continue

    return results
