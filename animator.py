from typing import Callable, Generic
from typing import TypeVar, Optional


TAnimVar =TypeVar('TAnimVar')

class Animator(Generic[TAnimVar]):
    def __init__(
            self,
            animation_var_init_val: TAnimVar,
            anim_var_update_fn: Callable[[TAnimVar], bool],):
        self._animation_var = animation_var_init_val
        self._anim_var_update_fn = anim_var_update_fn
        self._is_stopped = False

    def step(self):
        pass

    def stop(self):
        self._is_stopped = True

class AcceleratedAnimator(Animator, Generic[TAnimVar]):
    def __init__(
            self,
            anim_var_init_val: TAnimVar,
            anim_var_init_velocity: TAnimVar,
            anim_var_acceleration: TAnimVar,
            anim_var_update_fn: Callable[[TAnimVar], bool],
    ):
        super().__init__(anim_var_init_val, anim_var_update_fn)
        self._animation_var_velocity = anim_var_init_velocity
        self._animation_var_acceleration = anim_var_acceleration

    def step(self):
        if self._is_stopped:
            return

        self._animation_var_velocity += self._animation_var_acceleration
        self._animation_var += self._animation_var_velocity

        if self._anim_var_update_fn is not None:
            self._anim_var_update_fn(self._animation_var)


