from abc import ABC, abstractmethod


class EmailServiceInterface(ABC):

    @abstractmethod
    def send_mail(self, subject: str, recipient_list: list, context: dict, template_name: str, attachment: list = None):
        pass