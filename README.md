# send_login_mail
This script is used for sending an email with geolocalization.  
If launched in combo when a specific user login via ssh on the server, it is really helpful to track the login position by the user.
## Required packages
If you use your own server as SMTP server to send emails, you need to have the required packages to do so.
## Email's sample output
![Example_Output](https://github.com/AKAlex92/send_login_mail/blob/master/src_README/Sample_output.png)
## How to setup the script
First of all you need to setup the configuration file **login_email_conf.ini** with the needed parameters
* API_ACCESS_KEY: the API key used for the geolocalization service (in our case https://ipstack.com/).  
 You can get it freely with a previous sign up from https://ipstack.com/signup/free.
* SMTP_HOST: the host used by the SMTP library for sending email (if you are using your own machine to send email, set it as localhost). 
* EMAIL_FROM: the "from" parameter for sending email.
* EMAIL_TO: the "to" parameter for sending email.
* EMAIL_SUBJECT: the "subject" parameter for sending email. This will set the fixed subject of the email.
* HTML_TEMPLATE_FILE: path of the template file that actually contain the email's body saved in html format (default: login_email_template.html). This is a template file, and obviously, it has his own templates rules/variables.   The file **MUST** contains only html and css languages and, for being dynamic, needs to respect the templating rules.
## How to use
It is possible just to launch it as a normal python script:
```
./send_login_mail.py
```
Or  
```
python3 send_login_mail.py
```
  
It is also possible run it everytime you connect via ssh with a specific user.
To do so you just need to login with the user you are going to connect, edit your ~/.profile or ~/.bashrc file and, at the end of the file, add the following command line:
```
python3 /path/where/is/the/script/send_login_mail.py
```
Or just run this command:
```
echo "python3 /path/where/is/the/script/send_login_mail.py" >> ~./profile
```
Or
```
echo "python3 /path/where/is/the/script/send_login_mail.py" >> ~./bashrc
```
Being careful to replace "/path/where/is/the/script/" with the correct path where the script is saved.
## Authors

* **Alessandro Ripa (AKAlex92)** - *Initial work* - [send_login_mail] (https://github.com/AKAlex92/send_login_mail/)
