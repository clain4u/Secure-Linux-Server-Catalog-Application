# Catalog-udacity
A python flask application to implement an item catalog web application where user can read / write/ edit / delete items and provide provide read only JSON endpoints.

### Prerequisites
Linux Server [Ubuntu], Apache Python, PostgreSQL

## Getting Started
This project make use of Amazon Lightsail running ubuntu 16.04
### Linux Server configuration
 The setup will guide through the following steps.
 * Configure a user with sudo [root] permissions
 * Key pair authentication 
 * Configure Firewall
 * Configure Apache
 * Setup Python Virtual Environment
 * Setup PosgreSQL Database

#### Configure User
From the Amazon Lightsail terminal lets create new user with adduser command,
lets the user be ``` grader ``` for example.
```$ sudo adduser grader ```
Enter the password and user details when prompted for.
##### Add user to sudoers list
Add the ```grader``` user  to sudoers list with the following command
```sudo nano /etc/sudoers.d/grader```
This will open up a new file that defines permissions for the user "grader",
add the below lines, save and exit the file editor' 
```
grader ALL=(ALL) NOPASSWD:ALL
```
You can now login to the new user with the command
```$ su grader ``` enter password and check for yourself if the user have sudo permissions.

#### Key Pair authentication
Its vital for any server to disable password based authentication for security.
For this project we use key pair authentication method for added security.

From your local linx machine run the following command to generate a keypair
```$ ssh-keygen ```
Enter the name when prompted for, make sure the path falls into your ```.ssh``` directory,
this is mostly located inside your home directory, if it does not exist , please create one 
using ``` mkdir .ssh ```

Our final path would look like this for example .
``` /home/clain/.ssh/userGrader ``` 
for additional security you can add a password for the keyfile or leave empty for none.
This will generate the keypair files inside our .ssh directory whiche are
'userGrader' and 'userGrader.pub'

From within the server terminal window, create a new directory .ssh
```$ mkdir .ssh ``` and create a new file with touch command
```$ touch .ssh/authorized_keys ```

Ppen the file for editing ``` $sudo nano .ssh/authorized_keys ```  
now copy the contents from 'userGrader.pub' file and paste it within the authorized_keys file
save and exit.

Set file permissions so that other users canot access it 
```
$ chmod 700 .ssh
$ chmod 644 .ssh/authorized_keys
```
##### Disable SSH Password authentication
For added security lets disable passwod based authentication within ssh, to do that lets edit the ssh config file
```$sudo nano /etc/ssh/sshd_config ```
find the entry that reads ``` PasswordAuthentication ``` and set it to ``` PasswordAuthentication no ```

##### Change the default SSH port
Change the default ssh port to say ``` 2200 ``` as a point of security measure.
Within the same sshd_config file find the entry that reads ``` Port 22 ``` and change it to ``` Port 2200 ```
save the file and exit. Seload the ssh service using ``` $ sudo service ssh restart ```

##### Login using key pair
login to the server using the following command
```$ ssh grader@13.234.170.208 -p 2200 ```
where "grader" is the user , "13.234.170.208" is the IP address of your server and "-p 2200" defines the ssh port.
This will login you to the server terminal immediatly, if you have set a passoword for the key file you need to enter it for file access.

### Configure Firewall
Now that we have succesfully setup the key pair authentication lets setup the firewall. Ubuntu comes with a preinstalled
firewall "UFW" wihich is in a decativated state by default. You can check the status by typing ``` $ sudo ufw status ```

Now lets define the incoming and outgoing policys.  For security reasons lets deny all incoming sessions
``` $ sudo ufw default deny  incoming ```
 Now you will get a message that reads
``` 
Default incoming policy changed to 'deny'
(be sure to update your rules accordingly)
```
Lets allow all outgoing sessions
```$ sudo ufw default allow outgoing ```
This will output the following
```
Default outgoing policy changed to 'allow'
(be sure to update your rules accordingly)
```
Now that we have configured the default rules lets allow the ports that are necessary for our server.
We need to allow
* SSH on port 2200
* HTTP on port 80
* NTP on port 123

and deny the 
* Default ssh port 22

Lets execute the commands one by one 
```
$ sudo ufw allow ssh
$ sudo ufw allow 2200/tcp
$ sudo ufw allow www
$ sudo ufw allow ntp
$ sudo ufw deny 22
$ sudo ufw deny 22/tcp
```
 Now that we have configured the firewall , lets enable it.
 ``` sudo ufw enable ```
 You can check the status and it should display the following
 ```
 Status: active

To                         Action      From
--                         ------      ----
22                         DENY        Anywhere                  
2200/tcp                   ALLOW       Anywhere                  
80/tcp                     ALLOW       Anywhere                  
123/tcp                    ALLOW       Anywhere                  
22/tcp                     DENY        Anywhere                  
123                        ALLOW       Anywhere                  
22 (v6)                    DENY        Anywhere (v6)             
2200/tcp (v6)              ALLOW       Anywhere (v6)             
80/tcp (v6)                ALLOW       Anywhere (v6)             
123/tcp (v6)               ALLOW       Anywhere (v6)             
22/tcp (v6)                DENY        Anywhere (v6)             
123 (v6)                   ALLOW       Anywhere (v6)
 ```
 
 

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
* [Font Awesome ](https://fontawesome.com/)

## Author

Clain Dsilva - Catalog Udacity Project

## License

This project is licensed only to be used by Udacity FSND mentors.

## Acknowledgments

* The Atom editor , without which the coding is a mess.
* The whole Udacity batchmates and metors
* The Linux Mint - the OS I work on.
* My wife & kids - the great inspiration.