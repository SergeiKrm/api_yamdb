from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


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
