<h1 align="center">IT Inventory</h1>

<h3 align="center"> IT Inventory is a CMDB application inspired by the need to replace an Excel file as a tool. </h3>

<br>

The main goal of the program is to facilitate the management of hardware devices in small organizations. The organization supports the creation of businesses, with each business being owned by the user who created it, and only they have CRUD operations over that business. All other businesses not created by the specific user are visible for reading only. The devices created within a specific business are owned by the user who created the business, and again, only they can modify them. The Supplier section can be modified by all users, as there may be common suppliers for different businesses/locations.
<br>
<br>
After launching the application, the first registered user becomes a superuser and creates one time an organization to which all created businesses are connected. All other newly registered users have staff status, and they can only manage the businesses they have created.

- ### Build with:

  - ![Django](https://img.shields.io/badge/Django-092E20)
  - ![Python](https://img.shields.io/badge/Python-3670A0)
  - ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169e1)
  - ![JavaScript](https://img.shields.io/badge/JavaScript-ECDB6F)
  - ![Bootstrap](https://img.shields.io/badge/Bootstrap-850EF6)
  - ![HTML](https://img.shields.io/badge/HTML-F17545)
  - ![CSS](https://img.shields.io/badge/CSS-2964F2)

- ### To run the project:

  - run docker-compose.yml

  ```powershel
  docker-compose -f docker-compose.yml up
  ```

  - start the app

  ```powershell
  python manage.py runserver
  ```

  - start celery

  ```powershell
  celery -A inventory worker --loglevel=info --concurrency=2 -P solo
  ```

  - start celery beat

  ```powershell
  celery -A inventory beat --loglevel=info
  ```

- ### Full project description at this [link](./description/description.md)

- ### You can try the app on https://itinventoryazure.azurewebsites.net/
    <p>(the version is outdated, mising weekly sent report functionality)</p>

<br>
<br>

<h6 align="center"> Made with by Anton Petrov </h6>
