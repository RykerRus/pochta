# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from warnings import warn

class Mail:
    
    def __init__(self, mail=None):
        
        self.msg = MIMEMultipart()
        if mail is not None:
            self._creat_msg(mail)
    
    def _creat_msg(self, mail):
        if isinstance(mail, MIMEMultipart):
            self.msg = mail
        elif isinstance(mail, dict):
            for key, value in mail.items():
                print(key, value)
                setattr(self, key, value)
            
    @property
    def text(self):
        return self.msg.get("")

    @text.setter
    def text(self, value):
        self.msg.attach(MIMEText(value, "plain"))
    
    @property
    def html(self):
        return self.msg.as_string()

    @html.setter
    def html(self, value):
        self.msg.attach(MIMEText(value, "html"))
    
    def add_file(self, file_name):
        with open(file_name, "rb") as f:
            attachment = MIMEApplication(f.read())
        # Необходимо обозначить, что это вложение и его имя
        attachment.add_header("Content-Disposition", "attachment", filename=file_name)
        self.msg.attach(attachment)
        
    @property
    def tittle(self):
        return self.msg["Subject"]

    @tittle.setter
    def tittle(self, value):
        self.msg["Subject"] = value

    @property
    def email_from(self):
        return self.msg["From"]

    @email_from.setter
    def email_from(self, value):
        self.msg["From"] = value

    @property
    def email_to(self):
        return self.msg["To"]

    @email_to.setter
    def email_to(self, value):
        self.msg["To"] = value
