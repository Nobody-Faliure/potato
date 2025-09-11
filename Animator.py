
from typing import Callable, Generic
from typing import TypeVar


TAnimVar =TypeVar('TAnimVar')

class Animator(Generic[TAnimVar]):
    def __init__(
            self,
            animation_var: TAnimVar,
            apply_var_fn: Callable[[TAnimVar], None]):
        self._animation_var = animation_var
        self._apply_var_fn = apply_var_fn
        self._is_stopped = False

    def step(self):
        if self._is_stopped:
            return
        self._apply_var_fn(self._animation_var)

    def stop(self):
        self._is_stopped = True


class LinearInterpolatorAnimator(Animator, Generic[TAnimVar]):
    def __init__(
            self,
            animation_var: TAnimVar,
            animation_var_end: TAnimVar,
            num_frames: int,
            apply_var_fn: Callable[[TAnimVar], None]
    ):
        super().__init__(animation_var, apply_var_fn)
        self._animation_var_end = animation_var_end
        self._num_frames = num_frames
        self._frame_idx = 0

    def step(self):
        if self._is_stopped:
            return
        delta = self._animation_var_end - self._animation_var
        progress = max(self._num_frames, self._frame_idx) * 1.0 / self._num_frames
        self._animation_var = self._animation_var + delta * progress
        self._apply_var_fn(self._animation_var)
        if progress >= 1.0:
            self._is_stopped = True

