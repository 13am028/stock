# Vending Machine Tracking Application
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=13am028_stock&metric=coverage)](https://sonarcloud.io/summary/new_code?id=13am028_stock)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=13am028_stock&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=13am028_stock)
### Running
#### With Docker
    docker compose up
- use url = os... in backend.py
- edit environment variables in docker-compose.yml
- everything configured for you

#### Without Docker
    python backend.py
- initiate database by yourself
- hardcode the database user & password

** Main branch has frontend built in **
To get simple version without UI, checkout branch 'simple'

### Functions
* Home Page
  * go to location page / product page
* Location Page
  * see all locations (navigate to stock page when clicked)
  * add a new location
* Product Page
  * see all products
  * add a new product
* Stock Page
  * List all products in the vending machine given location
  * Click ${location_name} to go to Edit Location Page.
  * Increase / Decrease stock
  * Delete s product from the vending machine
* Edit Location Page
  * Change the name of the location
  * Delete Location
