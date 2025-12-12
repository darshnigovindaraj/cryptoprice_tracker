import yagmail

SENDER_EMAIL = "enter your email"
APP_PASSWORD = "enter your password"
RECEIVER_EMAIL = "enter an another email to send the alert"

def send_email(subject, body):
    yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
    yag.send(to=RECEIVER_EMAIL, subject=subject, contents=body)
    print("📧 Email sent successfully!")
