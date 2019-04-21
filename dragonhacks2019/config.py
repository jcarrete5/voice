import json


class Config:
    def __init__(self, file=None):
        with open(file) as cfg_file:
            self._cfg = json.load(cfg_file)
        self._scopes = [scope for scope in self._cfg['scopes']]
        self._scope_index = 0
        self._current_scope: dict = self._scopes[0]

    def next_scope(self) -> bool:
        """
        Increments the current scope. Returns `True` if successful,
        otherwise `False`.
        """
        if self._scope_index + 1 >= len(self._scopes):
            return False
        self._scope_index += 1
        self._current_scope = self._scopes[self._scope_index]
        return True

    def prev_scope(self) -> bool:
        """
        Decrements the current scope. Returns `True` if successful,
        otherwise `False`.
        """
        if self._scope_index - 1 < 0:
            return False
        self._scope_index -= 1
        self._current_scope = self._scopes[self._scope_index]
        return True

    def actions(self, phrase: str) -> list:
        """
        Returns the actions to be executed when the `phrase` is said
        or an empty list if the `phrase` isn't recognized.
        """
        return self._current_scope.get(phrase, [])

    def phrases(self) -> set:
        """
        Return the possible phrases that can be said in the current
        scope.
        """
        return set(phrase for phrase in self._current_scope.keys())


state = Config('format.json')
print(state.phrases())
