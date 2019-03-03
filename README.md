# catalog-udacity
A python flask application to implement an item catalog web application where user can read / write/ edit / delete items and provide provide readonly JSON endpoints.

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

this will install the new linux virtual machine.
Once setup you can start vagrant with the following command

```$ vagrant ssh```

### Database
This program makes use of SQLite database. Please find the sample database file 'catalog.db' in the project root folder.
The sample is provided as it is to test the program or for a quick run, You are encouraged to delete the sample database and 
make a fresh start after familiarising with the application.

#### Database Setup 

To setup a fresh database navigate to project root folder and run the "database_setup.py"
 ``` $ python database_setup.py ```
This will create an empty database and makes the application ready for a fesh start.

## Python Program 

Copy this program directory under vagrant folder so that its accessible the to the VM.
Change the directory in terminal to program directory 
```$ cd log_analysis ```
Your teminal should display the below path
``` vagrant/log_analysis $ ```

### Executing the Program

Execute using the following command in the terminal

``` python catlogz.py ```
This will bring up the webserver on port 5000 , your terminal should display the following
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
The catlog application provides an easy to use web based user interface that lits the categories and products for a public user, This section covers the UI details for the public user interface.

#### Basic navigation
* The catlog application lists the available categories on the left menu panel [common for all pages]
* select [click / navigate] the desired category to bring up the categroy page that lists the products in that category.
* Once in category page select any of the product listed to bring up the product page

##### Home page
Home page displays the **latest products** in the content area. Each product displays produt name, price and catgroy details. The users can click on the desired product to reach the product page, or the users can choose a desired category from the left navigation menu. 

##### Category page
The category page displays the products within the category. Each product displays produt name, price and catgroy details. The users can click on the desired product to reach the product page.

#### Product Page
The product page displays the produt name, price, catgroy and a detailed product description.

### User Interface for Registered User [UI]
The registerd / logged in user get access to all of the public user pages with the below additional features.
* Create new categories and Products
* Edit categories and Products 
* Delete categories and Products

##### Login and Logout
The catlog app allows the users to login via Google accounts 
* To login , click on the login button towards the top right corner of the application
* This will bring up the login page , once you have succesfully validated with google account, you wull be redirected to the home page that displays your logged in username and profile image towards the top right corner
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
Note: You need atleast one category created before you can start adding products 

#### Edit Category
To edit a category, 
* Navigate to desired category page 
* Click on the edit button [next to the category name ] , this will take the user to category edit page
* Edit categroy name and submit the page
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



