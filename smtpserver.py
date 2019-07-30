import smtplib
from warnings import warn

_SERVER_MAPPING = {"gmail" : {"server":"smtp.gmail.com", "port": 587}}


class SMTPServer:
    def __init__(self, user, server_name):
        self.user = user
        self.setup_server(server_name)
        self.__cached__ = None
    
    def open(self):
        self.connect_server()
        self.log_on()
        return self
    
    def __enter__(self):
        return self.open()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
    
    def setup_server(self, server_name):
        self.server, self.port = _SERVER_MAPPING[server_name].values()

    def connect_server(self):
        try:
            self.__cached__ = smtplib.SMTP(self.server, self.port)
            self.__cached__.starttls()
        except smtplib.SMTPException as err:
            warn(f"Ошибка при отправке письма: {err}")
        print("_connect_server")
    
    def log_on(self,):
        try:
            self.__cached__.login(self.user.login, self.user.password)
        except smtplib.SMTPException as err:
            warn(f"Ошибка при отправке письма: {err}")
        print("_log_on")
    
    def quit(self):
        if self.__cached__ is None:
            return
        try:
            self.__cached__.quit()
        except Exception as err:
            warn(f"Ошибка при Закрытии сервера: {err}")
    
    def send(self):
        try:
            self.__cached__.send_message(self.user.mail.msg)
            print("Письмо успешно отправлено!")
        except smtplib.SMTPException as err:
            warn(f"Ошибка при отправке письма: {err}")
    
    def multi_send(self, emails):
        try:
            self.__cached__.sendmail(self.user.login, emails, self.user.mail.msg.as_string())
            print("Письмо успешно отправлено!")
        except smtplib.SMTPException as err:
            warn(f"Ошибка при отправке письма: {err}")