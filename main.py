from github import Github
import smtplib
from email.mime.text import MIMEText
import ConfigParser
import boto3

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

subject = 'Github Name Missing'

emailmessage = 'You should really fill out your name on your GitHub account by going to https://github.com/settings/profile'

g = Github(githubusername, githubpassword)

org = g.get_organization(githuborgname)


members = org.get_members()

emaillist = []

f=open("NamelessUsers.txt","w+")

for member in members:
	if (member.name is None and member.email is not None):
		f.write(member.login + ' ' + member.email)
		emaillist.append(member.email)


f.close()

try:
	server = smtplib.SMTP(smtprelay + ':' + smtpport)
	server.ehlo()
	server.starttls()
	server.login(smtpusername, smtppassword)

	for email in emaillist:
		message = 'From %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s' % (fromaddress, email, subject, emailmessage)
		server.sendmail(fromaddress, email, message)
	server.quit()
	print 'Emails Sent!'
except smtplib.SMTPException, error:
	print str(error)
	print 'An error occurred when trying to send emails. Please check your Settings.ini and try again'


s3 = boto3.client('s3', aws_access_key_id = awskeyid, aws_secret_access_key = awssecret)

s3.upload_file('NamelessUsers.txt', awsbucket, 'NamelessUsers.txt')
