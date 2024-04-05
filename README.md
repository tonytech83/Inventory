# IT Inventory
IT Inventory is a CMDB application inspired by the need to replace an Excel file as a tool.


After launching the application, the first registered user becomes a superuser and creates one time an organization to which all created businesses are connected. All other newly registered users have staff status, and they can only manage the businesses they have created.

### To run the project:
- You shound have docker
  
  - run docker-compose.yml
    ```powershel
    docker-compose -f docker-compose.yml up
    ```
  - start celery
    ```powershell
    celery -A inventory worker --loglevel=info
    ```
  - start the app
    ```powershell
    python manage.py runserver
    ```

Full project description at [this link](./description/description.md)

You can try the app on https://itinventoryazure.azurewebsites.net/
