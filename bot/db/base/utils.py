import re

camel_to_snake_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_snake(string):
    snake = camel_to_snake_pattern.sub('_', string).lower()
    return snake
