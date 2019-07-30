from warnings import warn

from .mail import Mail
from .smtpserver import SMTPServer
from .imapserver import IMAPServer

_FROM_USERS = {
                "tester": {"login": "tester@imaginweb.ru", "password": ">3jEFybD>3jEFybD"},
                "al": {"login": "al8594212@gmail.com", "password": "QLTj698rm6T6BVz"}}

class User:
    def __init__(self, name, server_name="gmail"):
        self.name = name
        self._load_login_and_password()
        self.mail = None
        self.imap = IMAPServer(self, server_name)
        self.smtp = SMTPServer(self, server_name)

    def __str__(self):
        return f"< User: {self.name} | login: {self.login} | password:  {self.password} >\n<mail {self.mail}>"

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.imap.quit()
        self.smtp.quit()
    def _load_login_and_password(self):
        self.login, self.password = _FROM_USERS[self.name].values()
    
    def new_mail(self, mail=None):
        self.mail = Mail(mail=mail)
    
    def validation_email(self, email):
        if isinstance(email, str):
            return "@" in email and "." in email
        return False
    
    def send(self, to, server_name="gmail"):
        if self.mail is None:
            warn("Error: mail no create, Please call User.new_mail method")
        
        if self.validation_email(to):
            self.mail.email_from = self.login
            self.mail.email_to = to
            self.smtp.send()
                
        elif isinstance(to, list):
            self.mail.email_to = ",".join(to)
            self.smtp.multi_send(to)
    
    def get_mail(self, server_name="gmail"):
        self.imap.open()
        mail = self.imap.get_mail()
        return mail