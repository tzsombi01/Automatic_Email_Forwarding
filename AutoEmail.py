from email.message import EmailMessage
import smtplib, ssl
import email, imaplib
import time
# Standard details, emails, servers, port number
sender_email = "myEmail@gmail.com"
target_emails = ["emailToForwardTo@gmail.com"]
emailAddressesToForwardFrom = ["emailToForwardFrom1@gmail.com", "emailToForwardFrom2@gmail.com", "emailToForwardFrom3@gmail.com"]
password = input(str("Type the Password: ")) # 2 factor authentication: Use App Codes
SERVER_IMAP = "imap.gmail.com"
SERVER_SMTP = "smtp.gmail.com"
smtp_port = 465


def sendAnEmail(message):
	emailToSend = EmailMessage()
	try:
		emailToSend["From"] = sender_email
		emailToSend["CC"] = message["CC"]
		# emailToSend["SCC"] = message["SCC"]
		emailToSend["Header"] = message["Header"]
		emailToSend["Subject"] = message["Subject"]

		for part in message.walk():
			if part.get_content_type() == "text/plain":
				emailToSend.set_content(part)
			elif part.get_content_type() == "multipart/mixed":
				emailToSend.set_content(part.as_string())
			else:
				emailToSend.set_content(message)

		print("Details Gathered!")

	except Exception as e:
		pass

	# We open the SMTP connection, no need to close it, because of "with" keyword
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(SERVER_SMTP, smtp_port, context=context) as server:
		server.login(sender_email, password)
		for target_email in target_emails:
			server.sendmail(sender_email, target_email, emailToSend.as_string())
			print(f"Email has been sent to {target_email}")


mail = imaplib.IMAP4_SSL(SERVER_IMAP)
try:
	mail.login(sender_email, password)
	print("Login successful! ")
	print("------------------------------------------------------------------------------------")

	mail.select('INBOX')
	for emailAddress in emailAddressesToForwardFrom:

		_, msgnums = mail.search(None, f'(FROM {emailAddress} UNSEEN)')

		try:
			for msgnum in msgnums[0].split():
				_, data = mail.fetch(msgnum, '(RFC822)')
				message = email.message_from_bytes(data[0][1])

				sendAnEmail(message)
		except Exception as e:
			continue
	mail.close()
	mail.logout()

except Exception as e:
	pass
