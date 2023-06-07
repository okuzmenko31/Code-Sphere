from apps.followings.models import Following
from django.urls import reverse
from notifications.signals import notify
from abc import ABC, abstractmethod


class NotificationMessages(ABC):
    _notification_message = ''

    @property
    def notification_message(self) -> str:
        return self._notification_message

    @notification_message.setter
    @abstractmethod
    def notification_message(self, message: str, *args, **kwargs) -> str:
        """
        This method must return notification message.

        :return: str message.
        """
        raise NotImplementedError


class NotificationsMixin(NotificationMessages):
    send_mail = False
    html_mail_message_template = None

    def send_notification(self, sender, receiver):
        pass

    def send_mass_notifications(self, sender, recipients: list):
        for recipient in recipients:
            notify.send(sender=sender, recipient=recipient, verb=self.notification_message)
