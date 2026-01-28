class GameState:
    vars = {}

    @classmethod
    def set(cls, key, value):
        cls.vars[key] = value

    @classmethod
    def get(cls, key, default=None):
        return cls.vars.get(key, default)
