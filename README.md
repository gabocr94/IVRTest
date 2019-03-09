#IVR Middleware test : Gabriel Barrantes Jara


Before start
---
Run requirements.txt to install every required library used in this project.

        pip install -r requirements.txt
        


Configure SETTINGS
--
A few lines in settings file must change in order to run your own instance of this project:

Change STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY for your own stripe account keys

Also change LOGGING file locations to your own logging folders

Configure Database credentials
--
This application uses MySQL/MariaDB to save data. 
In settings you must edit DATABASES line and change it to your database configuration.

Next, run django migrations to set up database configuration:

    cd IVRTest/src
    python manage.py migrate

After you configured everything, you are ready to test this application.


How to start
---
In your web browser, go to the following url:
    
       127.0.0.1:8000

By default at start, the application will display a form for testing purposes, you must fill
every field. You can use the following data to fill the form:

    amount: 500
    currency: usd
    card num: 5555555555554444
    cvc_num: 101
    exp month: 01
    exp year: 28
    
 This information will create a charge of 5$ at your stripe account linked to the application and display the
 response received from Stripe API.
 In case, some information is not correct, a message will be displayed with a basic description of the issue.
 
