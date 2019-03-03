# Catalog-udacity
A python flask application to implement an item catalog web application where user can read / write/ edit / delete items and provide provide read only JSON endpoints.

### Prerequisites

Virtual Box, Vagrant, Python, SQLLite

## Getting Started
To start with you need the virtual box installed.
you can download and install virtual machine from here based on your choice of operating system.

https://www.virtualbox.org/wiki/Download_Old_Builds_5_1

Supported version of Virtual Box to install is version 5.1. 
Newer versions do not work with the current release of Vagrant

### Vagrant

Download your copy of vagrant from here. 
https://www.vagrantup.com/downloads.html
and install it based on the your choice of operating system.

### Virtual machine [VM]

Download your copy of virtual machine from here 
https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip

or clone it from here 
https://github.com/udacity/fullstack-nanodegree-vm

Extract the fsnd-virtual-machine.zip

From terminal change directory to "FSND-Virtual-Machine/vagrant"
Start the VM with the command
 
```$ vagrant up```

this will install the new Linux virtual machine.
Once setup you can start vagrant with the following command

```$ vagrant ssh```

### Database
This program makes use of SQLite database. Please find the sample database file 'catalog.db' in the project root folder.
The sample is provided as it is to test the program or for a quick run, You are encouraged to delete the sample database and 
make a fresh start after familiarizing with the application.

#### Database Setup 

To setup a fresh database navigate to project root folder and run the "database_setup.py"
 ``` $ python database_setup.py ```
This will create an empty database and makes the application ready for a fresh start.

## Python Program 

Copy this program directory under vagrant folder so that its accessible the to the VM.
Change the directory in terminal to program directory 
```$ cd log_analysis ```
Your terminal should display the below path
``` vagrant/log_analysis $ ```

### Executing the Program

Execute using the following command in the terminal

``` python catlog.py ```
This will bring up the web server on port 5000 , your terminal should display the following
 ```
 Catalog app running at port:5000 Url- http://localhost:5000/catalog
 * Serving Flask app "catalog" (lazy loading)
 * Environment: production
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
Catalog app running at port:5000 Url- http://localhost:5000/catalog
 * Debugger is active!
 * Debugger PIN: 737-066-608
 ```
The program is now ready to use , open up the browser and point the url to
http://localhost:5000/catalog to access the catalog application.

### User Interface for Public User [UI] 
The catalog application provides an easy to use web based user interface that list the categories and products for a public user, This section covers the UI details for the public user interface.

#### Basic navigation
* The catalog application lists the available categories on the left menu panel [common for all pages]
* select [click / navigate] the desired category to bring up the category page that lists the products in that category.
* Once in category page select any of the product listed to bring up the product page

##### Home page
Home page displays the **latest products** in the content area. Each product displays product name, price and category details. The users can click on the desired product to reach the product page, or the users can choose a desired category from the left navigation menu. 

##### Category page
The category page displays the products within the category. Each product displays product name, price and category details. The users can click on the desired product to reach the product page.

#### Product Page
The product page displays the product name, price, category and a detailed product description.

### User Interface for Registered User [UI]
The registered / logged in user get access to all of the public user pages with the below additional features.
* Create new categories and Products
* Edit categories and Products 
* Delete categories and Products

##### Login and Logout
The catalog app allows the users to login via Google accounts 
* To login , click on the login button towards the top right corner of the application
* This will bring up the login page , once you have successfully validated with google account, you will be redirected to the home page that displays your logged in username and profile image towards the top right corner
* To logout mouse over the profile name or image and click on the logout link on the popover menu
* This will logout the user from the application and redirects to the home page

#### Create category
To create a category click on the "Add new category" button which available towards the top right content area on all pages.
* This will bring up the "Add new category" modal window 
* Enter the category name and submit the form
* This will create a new category 

#### Create Product
To create a product click on the "Add new product" button which available towards the top right content area on all pages.
* This will bring up a modal window 
* Enter the product details [name, price, description] , select the desired category and submit the form
* This will create the new product in desired category
Note: You need at least one category created before you can start adding products 

#### Edit Category
To edit a category, 
* Navigate to desired category page 
* Click on the edit button [next to the category name ] , this will take the user to category edit page
* Edit category name and submit the page
* This will instantly update the category

#### Edit product
To edit a product, 
* Navigate to desired product page 
* Click on the edit product button towards the bottom left, this will take the user to product edit page
* Edit Product details and submit the page
* The users can also change the category of the product to another category he has created
* This will instantly update the category

### Delete Category
To delete a category
* Navigate to desired category page and click on delete [ next to category name]
* This will take the user to the confirm delete page
* Once confirmed the category and its products are deleted

### Delete product
To delete a product
* Navigate to desired product page and click on delete product [ bottom left]
* This will take the user to the confirm delete page
* Once confirmed the product is deleted from the category

## JSON EndPoints
The catalog app provides read only endpoints for public, the endpoints are as follows
#### Categories EndPoint
```http://localhost:5000/catalog/categories/JSON```
This endpoint returns the list of available categories with the following fields
* ID
* Name
Below is the sample output for this request
```
{
  "categories": [
    {
      "id": 1, 
      "name": "Baby Store"
    }, 
    {
      "id": 2, 
      "name": "Mens Arena"
    }, 
    {
      "id": 3, 
      "name": "Teenage Fasions"
    }, 
    {
      "id": 4, 
      "name": "Ladies Outlet"
    }, 
    {
      "id": 5, 
      "name": "The Women Store"
    }, 
    {
      "id": 6, 
      "name": "The Vetrans Cave"
    }
  ]
}
```
#### Category Products EndPoint
**format**
```http://localhost:5000/catalog/category/<Category_ID>/JSON```
Note: Category_ID's can be fetched from the categories endpoint [see above]

Example
```http://localhost:5000/catalog/category/2/JSON```

This endpoint returns the list of all products with the following fields within the requested category.
* Name
* ID
* Price
* Description
* Category_ID
Below is the sample output for this request
```
{
  "category_products": [
    {
      "category_id": 2, 
      "description": "A high Quality Denim Jeens", 
      "id": 3, 
      "name": "New Port Jeens", 
      "price": "$123.00"
    }, 
    {
      "category_id": 2, 
      "description": "Keep your eyes safe and style unmatched. Now with UV protection ", 
      "id": 8, 
      "name": "Ray Ban Sun Glass", 
      "price": "$399.99"
    }
  ]
}
```
#### Single Product EndPoint
**format**
```http://localhost:5000/catalog/product/<Product_ID>/JSON```
Note: Product_ID can be fetched from the "Category Products" endpoint [see above]

Example
```http://localhost:5000/catalog/product/8/JSON```

This endpoint returns the a single product with the following fields.
* Name
* ID
* Price
* Description
* Category_ID
Below is the sample output for this request
```
{
  "product": {
    "category_id": 2, 
    "description": "Keep your eyes safe and style unmatched. Now with UV protection ", 
    "id": 8, 
    "name": "Ray Ban Sun Glass", 
    "price": "$399.99"
  }
}
```

## Scope of Expansion
The project is designed with a view to expand further, hence I have included dummy images, JavaScript & HTML Frameworks

##### Dummy images
I have used dummy product images that fetches the placeholder images from http://placehold.jp for the time being
Someday later I wish to expand this catalog project to have a product image module added.

##### AJAX-it
The jQuery and Bootstrap bundle is included with a vision to take the project to a complete asynchronous level of application where the users get a seamless experience.

#### Responsive
The bootstrap framework and the theme is designed with a vision to make the project 100 responsive 

While these are the plans for the future, **I encourage the users to fork the project and take it to the next level**
- - - 
## Built With
* [Python](https://www.python.org/)
* [FLASK](http://flask.pocoo.org/)
* [SQLite](https://www.sqlite.org)
* [jQuery](https://jquery.com/)
* [Bootstrap](https://getbootstrap.com/)

## Author

Clain Dsilva - Catalog Udacity Project

## License

This project is licensed only to be used by Udacity FSND mentors.

## Acknowledgments

* The Atom editor , without which the coding is a mess.
* The whole Udacity batchmates and metors
* The Linux Mint - the OS I work on.
* My wife & kids - the great inspiration.