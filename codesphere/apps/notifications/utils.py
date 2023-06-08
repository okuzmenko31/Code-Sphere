from notifications.signals import notify
from abc import ABC


class NotificationMessages(ABC):
    _notification_message = ''

    @property
    def notification_message(self) -> str:
        return self._notification_message

    @notification_message.setter
    def notification_message(self, message: str):
        """
        This method must return notification message and
        set _notification_message

        :return: str message.
        """
        self._notification_message = message


class NotificationsMixin(NotificationMessages):
    send_mail = False
    html_mail_message_template = None

    def send_notification(self, sender, receiver):
        pass

    def send_mass_notifications(self, sender, recipients: list):
        for recipient in recipients:
            notify.send(sender=sender, recipient=recipient, verb=self.notification_message)
