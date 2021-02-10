import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime
# Email you want to send the update from (only works with gmail)
fromEmail = 'sendmail'
# You can generate an app password here to avoid storing your password in plain text
# https://support.google.com/accounts/answer/185833?hl=en
fromEmailPassword = '***************'

# Email you want to send the update to
toEmail = 'recmail'

def sendEmail(h,t,c_t):
	msgRoot = MIMEMultipart('related')
	now = datetime.datetime.now().strftime("%m/%d %H : %M : %S")
	msgRoot['Subject'] = ('DHT Update : '+str(now)+" __humd : %2.2f %%" % h+" // temp : %2.2f C" % t+" // cpu temp : %2.2f C"% c_t)
	msgRoot['From'] = fromEmail
	msgRoot['To'] = toEmail
	msgRoot.preamble = 'Raspberry pi security camera update'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('Smart security cam found object')
	msgAlternative.attach(msgText)

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)

	#msgImage = MIMEImage(image)
	#msgImage.add_header('Content-ID', '<image1>')
	#msgRoot.attach(msgImage)

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(fromEmail, fromEmailPassword)
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
	smtp.quit()
