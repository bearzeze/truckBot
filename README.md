# **TruckBot Automation Web App**

### Fully functional app for the scraping data about loads and informing available drivers through automation

## **Distinctiveness and Complexity**

As the creator of my web application, I’ve designed a platform that stands out for its innovative approach to streamlining the logistics of truck loads automatically using Django and Javascript.

Regarding to the distictivness platform provides next things:

* **Innovative Automation**: truckBot app revolutionizes the logistics field by automating the load information gathering process. This automation is a game-changer, making the booking of truck loads swift and efficient.

* **Seamless Data Scraping**: This app has a unique feature that scrapes data from loads websites, gathering all necessary details like origin, pickup date, destination, delivery date, miles, weight and price. During the proccess app collects data regarding all available drivers (such as name and phone number) in the vicinity of the load’s origin.

* **Sending messages via Zoom**: After data is gathered, messages about loads are automatically sent via Zoom to the truck drivers 

* **Driver Network Growth**: By informing drivers about available loads, platform actively grows the network of drivers, increasing the chances of load acceptance.

Speaking of complexity there are several things :

* **Sophisticated Data Management**: App’s ability to manage and synthesize data from different sources, such as load details and drivers information, adds a layer of complexity.

* **Advanced Web Scraping**: Crafting algorithms to accurately scrape data requires complex programming skills and meticulous error handling, which is successfully implemented.

* **Intelligent Messaging System**: developed an automated messaging system capable of creating and dispatching personalized messages to drivers, which involves intricate logic and scripting technology.

* **Real-Time Processing**: ensuring that the app processes data in real-time to provide drivers with prompt load information adds to its computational intricacy.

* **Full Stack**: app combines the user interface, server-side operations, and automated processes into one system. It’s designed to handle everything from the visual part that users interact with, to the behind-the-scenes coding that makes the app work, and even the automated tasks that save time. Utilizing planning and organization through the programming skills were the key of success.


## **Files**
The application is built using the Django Python Framework for the backend and JavaScript for the frontend. For web scraping and automation tasks it leverages Python script techniques.

The backend consists of a Django project and one Django app called “truckBot” with a standard structure:

* *urls.py* - This file defines the routes for the application.

* *models.py* - In this file, four database models are defined: User, Load, Driver, and LogHistory. The User object, in addition to authentication properties, contains information necessary for logging into the app where loads are posted. This website will be scraped for load and driver details. The User object also includes the local path to the Zoom.exe file and the phone number needed for running Zoom without issues. The Load object stores all information about a load, from which a message is created and sent to the driver. The Driver object includes the driver’s phone number, name, and the load they are associated with. The LogHistory object refers to the load for which all drivers are informed.

* *admin.py* - This file registers the models so that administrator can easily access the data in the database.

* *serializers.py* - In this file, serialization of the LogHistory model is done to obtain JSON data smoothly.

* *views.py* - This file contains the core structure of the web app, with over 350 lines of code.

The automation process for scraping and sending messages is defined in the following Python files located in the Django app:

* *scrape.py* - This file provides headless scraping of the truck logistic website where user needs to be logged in. Scraping is done based on the load id. As a result it gathers data into database about load and all the drivers that are nearby the load origin.

* *zoom.py* - This file provides way of opening Zoom on local machine using User fields, and based on the data from the Load and Driver model, to construct the message and inform the drivers about the load.

Both processes have the possibility of being aborted. Scraping can be stopped by clicking the "Abort" button, while sending messages can be interrupted by pressing the "Esc" key. These instructions are clearly stated on the website for the user’s convenience. Program will remember where it stopped and where to start without repetiton.

Frontend consists of HTML templates, CSS file and JavaScript file:

* **Templates folder** -  Contains HTML files using the Jinja2 template engine.

* **Static folder** - Includes the style.css file for styling the page, along with Bootstrap 5.3, and the script.js file with various actions and fetching functions.


## **How To Use App**

In order to use app you need to have account for the specific website used for truck logistics, and to be logged into Zoom prior to using the app. So only specific users can use this website.


