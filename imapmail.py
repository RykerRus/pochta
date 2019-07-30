import imaplib
import email
import sys
from time import sleep
import datetime

class IMAPmail:
    def __init__(self, server, msg_id):
        self.server = server
        self.msg_id = msg_id
        self.__cached__ = None
    
    def _is_load(self):
        if self.__cached__ is None:
            return False
        return True
    
    def get_data(self):
        if self._is_load:
            response, self.__cached__ = self.server.__cached__.fetch(self.msg_id,
                                                          message_parts="(RFC822)")
            if response != "OK":
                print("Не удалось получить письмо №", self.msg_id)
        return self.__cached__
    
    
    @property
    def text(self):
        # Получение текста письма
        text, _, _ = self._get_message_info()
        return text

    def _get_part_info(self, part):
        """Получить текст сообщения в правильной кодировке.

        Параметры:
          - part: часть сообщения email.Message.

        Результат:
          - message (str): сообщение;
          - encoding (str): кодировка сообщения;
          - mime (str): MIME-тип.

        """
        encoding = part.get_content_charset()
        # Если кодировку определить не удалось, используется по умолчанию
        if not encoding:
            encoding = sys.stdout.encoding
        mime = part.get_content_type()
        message = part.get_payload(decode=True).decode(encoding, errors="ignore").strip()
    
        return message, encoding, mime

    def _get_message_info(self):
        """Получить текст сообщения в правильной кодировке.

        Параметры:
          - message: сообщение email.Message.

        Результат:
          - message (str): сообщение или строка "Нет тела сообщения";
          - encoding (str): кодировка сообщения или "-";
          - mime (str): MIME-тип или "-".

        """
        message_text, encoding, mime = "Нет тела сообщения", "-", "-"
        raw_message = self.get_data()[0][1]
        message = email.message_from_bytes(raw_message)
        
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() in ("text/html", "text/plain"):
                    message_text, encoding, mime = self._get_part_info(part)
                    break  # Только первое вхождение
        else:
            message_text, encoding, mime = self._get_part_info(message)
        return message_text, encoding, mime
    