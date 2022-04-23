#Author Teddy Kay
import sys 
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtCore import QUrl 
from PyQt5.QtWebEngineWidgets import QWebEnginePage
import bs4 as bs 
import os
import smtplib
from playsound import playsound
from twilio.rest import Client

#Stores login info 
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = os.environ.get('TWILIO_FROM_NUMBER')
MY_PHONE_NUMBER = os.environ.get('MY_PHONE_NUMBER')


# Function defining email setup
def email_user():
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = 'Item availiable'
        body = 'Product is now availiable'
        msg = f'Subject: {subject}\n\n{body}'

            # logging.info('Sending Email...')
        smtp.sendmail(EMAIL_ADDRESS, 'teddyk77@gmail.com', msg)

# Setup sound alarm
def play_sound():
    playsound('alarm.mp3')

# Setup Texting twillo service

def setup_twilio_client():
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    return Client(account_sid, auth_token)

def send_notification():
    twilio_client = setup_twilio_client()
    twilio_client.messages.create(
        body="item is available",
        from_=TWILIO_FROM_NUMBER,
        to=MY_PHONE_NUMBER
    )

# Setup browser function QtWebEngine that grabs the website
class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

# Main program that calls functions if a class does not exist on the product page
def main():
    page = Page('https://www.costco.com/.product.100763567.html')
    soup = bs.BeautifulSoup(page.html, 'lxml')
    
            
    if soup.find_all(class_="primary-button-v2bbb"): 
        while True:
            print("Tag Found")
            
                 
    else:
        send_notification(), email_user(), play_sound()
        
if __name__ == '__main__': main()