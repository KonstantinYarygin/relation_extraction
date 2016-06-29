import argparse
import os
import sys

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_LOGIN = 'bakgen.niifhm@gmail.com'
SMTP_PASSWORD = 'prostosahar'
SUBJECT_PREFIX = '[bakgen]'
RECEIVERS_INI_PATH = 'receivers_tmp.ini'


def get_lines(filename):
    with open(filename) as f:
        lines = f.readlines()

    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()

    return lines


def send_mail(receivers, subject, body, files=None):
    if files is None:
        files = []
    print('start sending email')
    msg = MIMEMultipart()
    msg["From"] = SMTP_LOGIN
    msg["To"] = str(receivers)
    msg["Subject"] = SUBJECT_PREFIX + ' ' + subject

    if len(files) > 0:
        for file_to_attach in files:
            if os.path.isfile(file_to_attach):
                ctype, encoding = mimetypes.guess_type(file_to_attach)
                if ctype is None or encoding is not None:
                    ctype = "application/octet-stream"

                maintype, subtype = ctype.split("/", 1)
                fp = open(file_to_attach, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)

                attachment.add_header("Content-Disposition", "attachment", filename=file_to_attach)
                msg.attach(attachment)
            else:
                body = body + "Can't found file" + file_to_attach

    msg.attach(MIMEText(body, 'html'))
    user = SMTP_LOGIN
    pwd = SMTP_PASSWORD
    from_email = SMTP_LOGIN

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(from_email, receivers, msg.as_string())
        server.close()
        print('Successfully sent the mail to \n %s \n' % (str(receivers)))

    except BaseException:
        print("Failed to send the mail")

if __name__ == '__main__':
    sys.dont_write_bytecode = True

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action='store', nargs='+', help='Recievers (seperate with space)',
                        required=True)
    parser.add_argument('-s', action='store', help='Subject')
    parser.add_argument('-b', action='store', help='Body')
    parser.add_argument('-f', action='store', nargs='+', help='Files (separate with space)', default=[])

    args = parser.parse_args()
    arg_receivers = list(args.r)
    arg_subject = str(args.s)
    arg_body = str(args.b)
    arg_files = list(args.f)

    send_mail(arg_receivers, subject=arg_subject, body=arg_body, files=arg_files)
