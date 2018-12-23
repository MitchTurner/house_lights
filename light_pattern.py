class LightPattern(object):
    lights = {}

    def show(self) -> dict:
        raise NotImplementedError('Pattern must implement \'show\' method.')

    def populate_lights(self, length: int) -> None:
        raise NotImplementedError('Pattern must implement \'populate_lights\' method.')

    def refresh(self) -> None:
        raise NotImplementedError('Pattern must implement \'update\' method.')
