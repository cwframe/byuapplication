from github import Github
import smtplib
import ConfigParser
import boto3

# Reading in the settings.ini file
config = ConfigParser.ConfigParser()

config.read('settings.ini')
githubusername = config.get('Settings', 'GithubUsername')
githubpassword = config.get('Settings', 'GithubPassword')
githuborgname = config.get('Settings', 'GithubOrgName')
smtprelay = config.get('Settings', 'SMTPRelay')
smtpport = config.get('Settings', 'SMTPPort')
smtpusername = config.get('Settings', 'SMTPUsername')
smtppassword = config.get('Settings', 'SMTPPassword')
fromaddress = config.get('Settings', 'FromAddress')
awskeyid = config.get('Settings', 'AWSAccessKeyID')
awssecret = config.get('Settings', 'AWSSecret')
awsbucket = config.get('Settings', 'AWSBucketName')

# setting up part of the email message
subject = 'Github Name Missing'
emailmessage = 'You should really fill out your name on your GitHub account by going to https://github.com/settings/profile'

# get the members of the given github org
g = Github(githubusername, githubpassword)
org = g.get_organization(githuborgname)
members = org.get_members()

emaillist = []

f=open("NamelessUsers.txt","w+")

for member in members:
	if (member.name is None and member.email is not None):
		# writes the member login and email to a file to be uploaded to AWS S3 bucket
		f.write(member.login + ' ' + member.email)
		# adds email to email list
		emaillist.append(member.email)


f.close()

# Sends email to users without usernames that have public emails
try:
	server = smtplib.SMTP(smtprelay + ':' + smtpport)
	server.ehlo()
	server.starttls()
	server.login(smtpusername, smtppassword)

	for email in emaillist:
		message = 'From %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s' % (fromaddress, email, subject, emailmessage)
		server.sendmail(fromaddress, email, message)
	server.quit()
	print 'Emails Sent'
except smtplib.SMTPException, error:
	print str(error)
	print 'An error occurred when trying to send emails. Please check your Settings.ini and try again'

# Uploads file of Nameless users to S3 bucket on AWS
s3 = boto3.client('s3', aws_access_key_id = awskeyid, aws_secret_access_key = awssecret)

s3.upload_file('NamelessUsers.txt', awsbucket, 'NamelessUsers.txt')

print 'File uploaded to AWS S3 bucket'

print 'Done'
