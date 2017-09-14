# byuapplication
github for an application to byu

This repo is for a job application for a Software Engineer postiion at BYU.

This program only uses tls to send emails over smtp.

It is designed to work with gmail, but can potentially work with other smtp servers.

This program is designed to run in python 2.7 and you must install the following packages using pip:
* boto3
* PyGithub

This program has a settings.ini file that must be filled out in order to run.
The following is an explanation of each setting:
* GithubUsername: Username used to log into github
* GithubPassword: Password used to log into github
* GithubOrgName: The name of the orginzation you wish to filter the users from
* SMTPRelay: smtp.gmail.com <- does not need to be changed if using gmail, otherwise it must be the smtp server address
* SMTPPort: 587 <- does not need to be changed if using gmail, but the port must use tls
* SMTPUsername: Your smtp username, for gmail it is the email address
* SMTPPassword: Password for smtp server
* FromAddress: Your email address
* AWSAccessKeyID: Obtained from the IAM console on AWS
* AWSSecret: Obtained from the IAM console on AWS
* AWSBucketName: The destination bucket's name for the list of nameless users

After setting up the settings.ini, the file will run by simply typing:
python main.py


Assumptions:
* The smtp server works with tls
* setting.ini has been filled out correctly
* The AWS access token gives write permissions to the given bucket
* The s3 bucket has already been created

If you have any questions please contact me.
