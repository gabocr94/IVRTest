#IVR Middleware test : Gabriel Barrantes Jara


Before start
---
Run requirements.txt to install every required library used in this project.

        pip install -r requirements.txt

Configure SETTINGS
--
A few lines in settings file must chnage in order to run your own instance of this project:

Change STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY for your own stripe account keys

Also change LOGGING file locations to your own logging folders

Configure Database credentials
--
This application uses MySQL/MariaDB to save data. 
In settings you must edit DATABASES line and change it to your database configuration.


After you configured everything, you are ready to test this application.