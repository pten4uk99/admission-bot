from architecture.base.button import CallBackInlineButton


def get_callback_data_name(button: CallBackInlineButton):
    class_name = button.__class__.__name__
    return f'{class_name}_{id(button)}'


