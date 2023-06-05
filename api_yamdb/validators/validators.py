from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomRegexValidator(RegexValidator):
    def __call__(self, value):
        try:
            super().__call__(value)
        except ValidationError as e:
            invalid_symbols = self.get_invalid_symbols(value)
            e.message = self.message % {'invalid_symbols': invalid_symbols}
            raise e

    def get_invalid_symbols(self, value):
        return ''.join([char for char in value if not self.regex.match(char)])


characters_validator = CustomRegexValidator(
    r'^[\w.@+-]+$',
    'Имя пользователя содержит недопустимые символы: %(invalid_symbols)s'
)


def username_not_me_validator(value):
    if value == 'me':
        raise ValidationError(
            _('Использовать имя "me" в качестве username запрещено!')
        )


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'Ошибка ввода года. Указан {value},'
            f'сейчас {timezone.now().year}.'
            'Введите корректный год!'
        )
