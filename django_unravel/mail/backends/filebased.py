import datetime
import os
import webbrowser

from django.conf import settings
from django.core.mail.backends.filebased import EmailBackend as DjangoEmailBackend
from django.template.loader import render_to_string


class EmailBackend(DjangoEmailBackend):
    """
    Email backend for Django that let you preview email on your web browser
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_filename(self):
        """Return a unique file name."""
        if self._fname is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            fname = f'{timestamp}-{abs(id(self))}.html'
            self._fname = os.path.join(self.file_path, fname)
        return self._fname

    def write_message(self, message):
        attachments = []
        if hasattr(message, 'attachments') and message.attachments:
            temporary_path = settings.EMAIL_FILE_PATH

            for attachment in message.attachments:
                if isinstance(attachment, tuple):
                    new_file = open(os.path.join(temporary_path, attachment[0]), 'wb+')
                    new_file.write(attachment[1])
                    attachments.append([attachment[0], new_file.name])
                    new_file.close()
                else:
                    new_file = open(
                        os.path.join(temporary_path, attachment.name), 'wb+'
                    )
                    new_file.write(attachment.read())
                    attachments.append([attachment.name, new_file.name])
                    new_file.close()

        if hasattr(message, 'alternatives') and message.alternatives:
            body = message.alternatives[0][0]
        else:
            body = message.body
        context = {'message': message, 'body': body, 'attachments': attachments}
        template_content = render_to_string('django_unravel/email.html', context)
        self.stream.write(template_content.encode('utf-8'))

    def close(self):
        super().close()
        webbrowser.open('file://' + self._fname)
