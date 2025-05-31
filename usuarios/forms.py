from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField

class CaptchaAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()