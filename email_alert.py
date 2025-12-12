import yagmail

SENDER_EMAIL = "darshnigovind2005@gmail.com"
APP_PASSWORD = "DARSHNIGOVINDARAJ@2005"
RECEIVER_EMAIL = "23cst008@vcew.ac.in"

def send_email(subject, body):
    yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
    yag.send(to=RECEIVER_EMAIL, subject=subject, contents=body)
    print("📧 Email sent successfully!")
