import smtplib
import requests
import cfg.config as cfg
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import agent.config.parameter as parameter


setting = cfg.get_cfg()
MAIL_NOTIF_LIST = setting['mail_notif_list']
SLACK_TOKEN = setting['slack_token']
SLACK_NOTIF_LIST = setting['slack_notif_list']
URL = setting['slack_url']


def send_slack_msg(msg, slack_notif_list=SLACK_NOTIF_LIST):
    for target in slack_notif_list:
        my_params = {
            'token': SLACK_TOKEN,
            'channel': target
        }
        r = requests.post(
            URL,
            params=my_params,
            data=msg.encode(),
        )


def send_mail(sub, content, attach_list, append_mail_str=''):
    gmail_user = parameter.NOTIF_SENDER_ACCOUNT()
    gmail_password = parameter.NOTIF_SENDER_PW()
    from_address = parameter.NOTIF_SENDER_ACCOUNT()
    global MAIL_NOTIF_LIST
    MAIL_NOTIF_LIST += append_mail_str.split(',')
    print(f'tex test ........{MAIL_NOTIF_LIST}')
    to_address = MAIL_NOTIF_LIST

    attachments = attach_list
    print(f'AT: [{attachments}]')

    mail = MIMEMultipart()
    mail['From'] = from_address
    mail['To'] = ', '.join(to_address)
    mail['Subject'] = sub
    # Add mail content
    mail.attach(MIMEText(content))
    # Add mail attachment
    for file in attachments:
        if os.path.exists(file):
            with open(file, 'rb') as fp:
                add_file = MIMEBase('application', "octet-stream")
                add_file.set_payload(fp.read())
            encoders.encode_base64(add_file)
            add_file.add_header(
                'Content-Disposition',
                'attachment',
                filename=file
            )
            mail.attach(add_file)

    # Use smtp to send mail
    smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_password)
    smtpserver.sendmail(from_address, to_address, mail.as_string())
    smtpserver.quit()

