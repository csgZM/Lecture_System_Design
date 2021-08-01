import smtplib
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login('<gmail_address>', '<gmail_password>')
server.sendmail('<from>', 'someone@gmail.com', '<message>')
