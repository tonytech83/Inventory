import random

from rest_framework.response import Response
from rest_framework import status

from inventory.devices.models import Device


def catches_exception(error):
    if 'serial_number' in str(error):
        return Response({'detail': 'UNIQUE constraint failed: devices_device.serial_number'},
                        status=status.HTTP_400_BAD_REQUEST)
    elif 'device_name' in str(error):
        return Response({'detail': 'The Device name is already used. Please use a unique Device name.'},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_400_BAD_REQUEST)


def create_devices_form_upload(sheet, business):
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
