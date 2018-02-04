from components.Provider import BaseProvider


class DefaultProvider(BaseProvider):
    def __init__(self):
        super(DefaultProvider, self).__init__()
        self.vars = {}

    def provider_name(self):
        return "Default_Provider"

    def set(self, key, value):
        if not isinstance(key, str):
            raise ValueError("Key can only be string.")
        self.vars[key] = value

    # if a string, returns value for that string.  if not a string, returns itself
    def get(self, key):
        return self.vars[key] if isinstance(key, str) else key
