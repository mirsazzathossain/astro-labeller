from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import user_passes_test
import six
import threading

class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_verified))

generate_token = TokenGenerator()
    

def send_activation_email(request, user):
    scheme = request.scheme
    domain_name = request.META['HTTP_HOST']
    email_subject = 'Verify Email Address'
    msg_plain = render_to_string('accounts/verification-mail.txt', {
        'protocol': scheme,
        'user': user,
        'domain': domain_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    email_body = render_to_string('accounts/verification-mail.html', {
        'protocol': scheme,
        'user': user,
        'domain': domain_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    
    email = EmailMultiAlternatives(email_subject, msg_plain)
    email.attach_alternative(email_body, "text/html")
    email.to = [user.email]
    email.from_email = 'Astro. Labeller'

    EmailThread(email).start()

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def login_forbidden(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url='app:home',
        redirect_field_name=""
    )
    if function:
        return actual_decorator(function)
    return actual_decorator