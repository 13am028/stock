# location
ALL_LOCATIONS_PATH = "/all_locations"
ADD_LOCATION_PATH = "/location/add-location"
CHANGE_LOCATION_NAME_PATH = "/location/change-location-name"
DELETE_LOCATION_PATH = "/location/delete-location"
EDIT_LOCATION_PATH = "/location/edit-location/<location_id>"

# product
ALL_PRODUCTS_PATH = "/all_products"
ADD_PRODUCT_PATH = "/product/add-product"
DELETE_PRODUCT_PATH = "/product/delete-product"

# stock
STOCK_DETAIL_PATH = "/stock/detail/<location_id>"
ADD_PRODUCT_TO_STOCK_PATH = "/stock/add-product-to-stock"
INCREASE_STOCK_PATH = "/stock/increase-stock"
DECREASE_STOCK_PATH = "/stock/decrease-stock"
DELETE_PRODUCT_FROM_STOCK_PATH = "/stock/delete-product-from-stock"

# timeline
STOCK_TIMELINE_PATH = "/stock-timeline"
GET_TIMELINE_BY_LOCATION = "/stock-timeline/timeline-by-location"
GET_TIMELINE_BY_PRODUCT = "/stock-timeline/timeline-by-product"

# html
BASE_TEMPLATE = "base.html"
EDIT_LOCATION_TEMPLATE = "edit-location.html"
LOCATION_TEMPLATE = "location.html"
PRODUCT_TEMPLATE = "product.html"
STOCK_TEMPLATE = "stock.html"
TIMELINE_TEMPLATE = "stock-timeline.html"
