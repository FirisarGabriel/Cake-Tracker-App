# Cake-Tracker-App
A cake tracker CRUD web app made with Flask and MongoDB

Installation

Before starting, ensure you have the following installed on your system:

Python
MongoDB
pip

Setup Instructions:

1. Clone the Repository

2. Install Flask and PyMongo
pip install flask
pip install pymongo

3. Database Setup
Start your MongoDB server on the default port (27017)

4. Run the Application
python app.py

The application should now be running locally. Open your web browser and go to http://localhost:5000 to access the Datavid Cake Tracker.

Usage:

Adding a New Member

1.Navigate to the homepage.
2.Click on the "Add New Member" link.
3.Fill out the form with the member's details (First Name, Last Name, Birth date, Country, City).
4.Click the "Submit" button.
5.The member will be added to the database, and you will be redirected to the homepage.

Viewing Members and Birthdays

On the homepage, all existing members are listed.
Each member entry displays their full name, birthdate, country, city, and a delete button.
The page also indicates the number of days until the next member's birthday, if any.

Deleting a Member

To delete a member, click the "Delete member" button next to their details.
Confirm the deletion in the prompt that appears.
