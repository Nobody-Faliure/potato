from enum import Enum

class GameSession:

    class GameSessionState(Enum):
        IN_GAME = 0
        DEAD = 1
        TITLE_SCREEN = 2

    def __init__(self):
        self._hp = 100
        self._game_session_state = self.GameSessionState.TITLE_SCREEN

    def get_hp(self) -> int:
        return self._hp

    def get_state(self) -> GameSessionState:
        return self._game_session_state

    def process_hp(self, hp_change_value: float) -> None:
        self._hp += hp_change_value
        if self._hp <= 0:
            self._game_session_state = self.GameSessionState.DEAD
            self._hp = 100

    def change_state(self, new_state: GameSessionState) -> None:
        self._game_session_state = new_state
