from django.core.exceptions import ValidationError
import re
import phonenumbers
from django.utils.translation import gettext_lazy as _



class PhoneValidators:
    requires_context = False


    @staticmethod
    def clean(value):
        return re.sub('[^0-9]+', '', value)


    @staticmethod
    def validate(value):
        try:
            z = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(z):
                return False
        except:
            return False

        if len(value) != 13 or not value.startswith('+998'):
            return False

        return True

    def __call__(self, value):
        if not PhoneValidators.validate(value):
            raise ValidationError(_("Kiritilgan qiymat telefon raqam emas iltimos tekshirip qaytadan kiriting"))
