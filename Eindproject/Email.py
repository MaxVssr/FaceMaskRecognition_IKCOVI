import email
import getpass
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = ""
password = ""
receiver_email = ""

def sendMail(foto):
    port = 587 # dit is de port voor de smtp server van gmail
    smtp_server = "smtp.gmail.com" # dit is de smtp mail server van gmail om mails over te kunnen versturen
    password = getpass.getpass(prompt="Enter your Sender (GMAIL) Password: ") #hier komt je wachtwoord
    sender_email = input("Enter your Sender (GMAIL) Email: ") #hier komt je email adress
    receiver_email = input("Enter the Receiver Email: ") #hier komt de receiver email adress
    subject = "Someone without a face mask is walking around in the building."
    body = "Someone without a face mask is walking around in the building. Recognise this person? Kindly ask them to wear one. :)"

    message = MIMEMultipart() # met MIME objects kun je emails maken in Python, hieronder worden de onderdelen van de email gedefinieërd
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    message.attach(MIMEText(body, "plain"))
    filename = foto

    attachment = open(filename, "rb") # hier wordt de foto die genomen is als attachment toegevoegd aan de email
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

    encoders.encode_base64(part) # encode de email via base64

    part.add_header("Content-Disposition", f"attachment; filename={filename}",)

    message.attach(part)
    text = message.as_string() # maakt de text een string

    context = ssl.create_default_context() # definieërd de context voor de mailserver en start ttls (beveiligde mailprotocol via smtp)
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def setEmailData():
    # zet de sender en receiver mail als global
    global sender_email
    global receiver_email

    # Het is mogelijk om de sender en receiver email in de SetEmails.txt, als je dit doet hoef je niet elke keer de emails 
    # in te vullen in de terminal en worden deze uit de file gepakt.
    emails = open('D:\Oud Bureaublad\School\Hogeschool Leiden\Jaar_3\IKCOVI\Eindproject\SetEmails.txt').readlines()
    if len(emails) > 2:
        # Hier moet gedefinieërd worden dat de eerste email in de SetEmail.txt file een gmail adres is, dit in verband met de gmail smtp server
        # Dit kan ook een mail adres prefix zijn als je een andere smtp server gebruikt.
        # Het tweede adres (de receiver) kan elk email adres zijn wat je wilt.
        if "@gmail.com" in emails[1] and "@" in emails[2]:
            askPassword()
            sender_email = emails[1]
            receiver_email = emails[2]
            return

    # Inputs voor het zetten van de email data
    sender_email = input("Enter your Sender (GMAIL) Email: ")  # hier komt je email address
    askPassword()
    receiver_email = input("Enter the Receiver Email: ")  # hier komt de receiver email address


def askPassword():
    # Zorgt ervoor dat het wachtwoord niet zichtbaar is in de terminal, ivm privacy
    global password
    password = getpass.getpass(prompt="Enter your Sender (GMAIL) Password: ")