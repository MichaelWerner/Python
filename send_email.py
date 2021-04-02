import smtplib
from email.message import EmailMessage

sender='me@sender.com'           #replace with email address
recipient=['you@recipient.com']  #must be a list, replace with email address(es)
subject='test'
body='This is a python email'
mailserver='sender.com'          #replace with mail server

msg = EmailMessage()             #create the message

#fill the fields
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = ', '.join(recipient)
msg.set_content(body)

sendit=smtplib.SMTP(mailserver)  #create mail server object
sendit.set_debuglevel(1)         #get detailed information
sendit.send_message(msg)          
sendit.quit()                    #that's it. Close the connection
