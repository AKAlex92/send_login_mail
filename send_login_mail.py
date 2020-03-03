#!/usr/bin/env python3

import smtplib # library for sending emails
from email.mime.multipart import MIMEMultipart # for creating message object to send from email
from email.mime.text import MIMEText

import sys, os # base libraries os, shell libraries
import subprocess # library for launch commands on shell
import socket # library used for obtaining my hostname
import datetime # library for handling time

import requests # library for make http requests
import json # library used for parsing json returned from the http response
from pathlib import Path # library used for handling files 
from string import Template  # library used for templating the html string of the email
import configparser  # library used for parsing configuration file
######################################################
# Setting configuration variables
configuration_filename = "login_email_conf.ini"
config = configparser.RawConfigParser(allow_no_value=False)
try:
	config.read(configuration_filename)
	api_key = config.get('base configuration', 'API_ACCESS_KEY')
	smtp_host = config.get('base configuration', 'SMTP_HOST')
	email_from = config.get('base configuration', 'EMAIL_FROM')
	email_to = config.get('base configuration', 'EMAIL_TO')
	email_subject = config.get('base configuration', 'EMAIL_SUBJECT')
	html_template_file = config.get('base configuration', 'HTML_TEMPLATE_FILE')
except (FileNotFoundError, configparser.Error, Exception) as e:
	print("Error while parsing configuration file %s\nError message: \n\t%s" % (configuration_filename, e.message))
	sys.exit(1)
######################################################
# Setting script variables
now = datetime.datetime.now()
hostname = socket.gethostname()
p = subprocess.Popen("echo $SSH_CONNECTION | awk '{print $1}'", stdout=subprocess.PIPE, shell=True) # To obtain the public ip of whom is connecting on the ssh service
out = p.communicate() # launch the command. Thanks to stdout=subprocess.PIPE, shell=True i can retrieve the output [PS: the output is a tuple, that's why [0] ]
tmp_ip = out[0]
# I use that service to get a json with information about that IP (https://ipstack.com/documentation)
send_url = 'http://api.ipstack.com/' + tmp_ip.decode("ascii").replace('\n', '') + "?access_key=" + api_key  #.decode("utf-8") because it's a byte string so i have to convert in string
response = requests.get(send_url)
j = json.loads(response.text)
if j['success'] is True:
	ip = j['ip']
	latitude = j['latitude']
	longitude = j['longitude']
	country_name = j['country_name']
	city = j['city']
	zip_code = j['zip']
	country_flag = j['location']['country_flag']
else:
	print("Error on API call: %s" % send_url)
	sys.exit(2)
######################################################

# defining parameters for sending email
mailpar = MIMEMultipart()
mailpar['From'] = email_from
mailpar['To'] = email_to
mailpar['Subject'] = email_subject
# parsing and replace templating items from html template file
try:
	file_buff = Path(html_template_file).read_text()
	html_string = Template(file_buff).substitute(hostname=hostname, logintime=now.strftime("%d/%m/%Y %H:%M:%S"), ip=ip, latitude=latitude, longitude=longitude, country_flag=country_flag, country_name=country_name, city=city, zip_code=zip_code)
except FileNotFoundError as e:
	print("Error while parsing html template file %s\nError message: \n\t%s" % (html_template_file, e))
	sys.exit(3)

body = MIMEText(html_string, 'html')
mailpar.attach(body)

try:
   smtpObj = smtplib.SMTP(smtp_host)
   smtpObj.ehlo()
   smtpObj.starttls()
   smtpObj.ehlo()
   smtpObj.sendmail(mailpar['From'], mailpar['To'], mailpar.as_string())         
   print ("Successfully sent email")
   smtpObj.close()
except (smtplib.SMTPException, socket.error) as e:
   print("Error: unable to send email\nError message: \n\t%s" % e)
   sys.exit(99)