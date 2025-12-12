import yagmail

SENDER_EMAIL = "xxx enter your email"
APP_PASSWORD = "yyy"
RECEIVER_EMAIL = "xxx "

def send_email(subject, body):
    yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
    yag.send(to=RECEIVER_EMAIL, subject=subject, contents=body)
    print("📧 Email sent successfully!")
