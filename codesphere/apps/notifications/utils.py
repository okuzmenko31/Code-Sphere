from notifications.signals import notify
from abc import ABC


class NotificationMessages(ABC):
    _notification_message = ''
    _description_message = ''

    @property
    def notification_message(self) -> str:
        return self._notification_message

    @notification_message.setter
    def notification_message(self, message: str):
        self._notification_message = message

    @property
    def description_message(self) -> str:
        return self._description_message

    @description_message.setter
    def description_message(self, description: str):
        self._description_message = description

    @property
    def addition_message(self) -> str:
        return 'CodeSphere - one of the best IT Community in Ukraine!'


class NotificationsMixin(NotificationMessages):
    send_mail = False
    html_mail_message_template = None
    use_description = False

    def send_notification(self, sender, recipient):
        notify.send(sender=sender, recipient=recipient, verb=self.notification_message)

    def send_mass_notifications(self, sender, recipients: list):
        for recipient in recipients:
            if not self.use_description:
                notify.send(sender=sender,
                            recipient=recipient,
                            verb=self.notification_message)
            else:
                notify.send(sender=sender,
                            recipient=recipient,
                            verb=self.notification_message,
                            description=self.description_message)
