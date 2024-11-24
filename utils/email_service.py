from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import threading
# from threading import Thread


# mass_mail for multi-group
def send_email(subject, to, template_name, context=None):
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email,
                  [to], html_message=html_message)
    except:
        return True


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content,
                           settings.EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


def send_email_api(subject, to, template_name, context=None):
    try:
        html_message = render_to_string(template_name, context)
        EmailThread(subject=subject, html_content=html_message,
                    recipient_list=[to]).start()
    except:
        pass
