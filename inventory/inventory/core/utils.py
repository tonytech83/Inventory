from rest_framework.response import Response
from rest_framework import status


def catches_exception(error):
    print(error)

    if 'serial_number' in str(error):
        return Response({'detail': 'UNIQUE constraint failed: devices_device.serial_number'},
                        status=status.HTTP_400_BAD_REQUEST)
    elif 'device_name' in str(error):
        return Response({'detail': 'The Device name is already used. Please use a unique Device name.'},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_400_BAD_REQUEST)
