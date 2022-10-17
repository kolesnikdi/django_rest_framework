import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# username = 'segareta'
# password = 'pNyBVB8lOlC4CfM5'
username = 'segareta@ukr.net'
password = '1879dadybad'


# todo: problems with send email. I think problem with logon to ukr.net, but i'm not sure
def send_mail(url=None, text='Email_body', subject='', from_email='', to_emails=[]):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    url_part = MIMEText(f'http://127.0.0.1:8000/registration/{url}')
    msg.attach(url_part)
    msg_str = msg.as_string()
    print(msg_str)

    server = smtplib.SMTP(host='smtp.ukr.net', port=465)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()

