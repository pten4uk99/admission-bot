from architecture.base import Keyboard, CallBackInlineButton

__all__ = [
    'SelectCourseKeyboard'
]


class GameFilmDirectorButton(CallBackInlineButton):
    text = 'Режиссер игрового кино'


class SoundDirectorButton(CallBackInlineButton):
    text = 'Звукорежиссер АВИ'


class ArtButton(CallBackInlineButton):
    text = 'Искусствовед'


class DramaButton(CallBackInlineButton):
    text = 'Драматург'


class ActorButton(CallBackInlineButton):
    text = 'Актер театра и кино'


class MovieButton(CallBackInlineButton):
    text = 'Киновед'


class SelectCourseKeyboard(Keyboard):
    button_classes = [
        GameFilmDirectorButton,
        SoundDirectorButton,
        ArtButton,
        DramaButton,
        ActorButton,
        MovieButton,
    ]
