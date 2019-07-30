import imaplib
import email
import sys
from time import sleep
import datetime

from warnings import warn

from .imapmail import IMAPmail

_SERVER_MAPPING = {"gmail": {"server": 'imap.gmail.com', "port": "993"}}


class IMAPServer:
    def __init__(self, user, server_name):
        self.user = user
        self.setup_server(server_name)
        self._select = None
        self.__cached__ = None
        self.online = False
        
    def open(self):
        if not self.online:
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
            self.__cached__ = imaplib.IMAP4_SSL(self.server, self.port)
        except Exception as err:
            warn(f"Ошибка при отправке письма: {err}")
        print("_connect_server")
    
    def log_on(self, ):
        try:
            self.__cached__.login(self.user.login, self.user.password)
            self.online = True
        except Exception as err:
            warn(f"Ошибка при отправке письма: {err}")
        print("_log_on")
    
    def select(self, mailbox='INBOX', readonly=False):
        self.__cached__.select(mailbox, readonly)
        self._select = mailbox
    
    def _get_mail_ID(self, criterion):
        if self._select is None:
            self.select()
        response, messages_nums = self.__cached__.search(None, criterion)
        print(response, self._select)
        if response != "OK":
            warn("Не удалось получить список писем.")
            return
        return messages_nums[0].split()
    
    def get_mail(self, criterion="ALL"):
        msg_id = self._get_mail_ID(criterion=criterion)
        return [IMAPmail(self, id_) for id_ in msg_id[::-1]]
        
    
    def quit(self):
        try:
            self.__cached__.logout()
            self.online = False
        except Exception as err:
            warn(f"Ошибка при отправке письма: {err}")
    