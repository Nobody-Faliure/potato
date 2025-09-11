from typing import Union, Optional

class Animation:
    def __init__(self):
        super().__init__()
        self._animations: dict[str, dict[str, Optional[Union[int, float, bool]]]] = {}

    def add_animation(self,
                      name: str,
                      increment: Union[int, float],
                      duration: Optional[int],
                      duration_per_increment: int,
                      recurring: bool,
                      reverse_at_end: bool,
                      animated_value: Union[int, float],
                      max_increment: int = None) -> None:

        if max_increment is not None:
            if increment > max_increment:
                increment = max_increment
            elif increment < -max_increment:
                increment = -max_increment

        self._animations[name] = {"increment": increment,
                                  "duration": duration,
                                  "duration_per_increment": duration_per_increment,
                                  "recurring": recurring,
                                  "reverse_at_end": reverse_at_end,
                                  "animated_value": animated_value,
                                  "initial_value": animated_value,
                                  "max_increment": max_increment,
                                  "duration_per_increment_count": 1}

    def process_animation(self, name: str) -> None:
        animation_info = self._animations[name]

        if animation_info["duration_per_increment_count"] >= animation_info["duration_per_increment"]:
            if animation_info["duration"] is not None:
                animation_info["duration_per_increment_count"] = 1
                if animation_info["duration"] <= 0:
                    if animation_info["recurring"] and animation_info["reverse_at_end"]:
                        raise "Cannot both recur and reverse for animations"
                    elif animation_info["recurring"]:
                        animation_info["animated_value"] = animation_info["initial_value"]
                    elif animation_info["reverse_at_end"]:
                        animation_info["increment"] *= -1
                    else:
                        del self._animations[name]
                        return

                 # process increment
            print(animation_info["increment"])
            animation_info["animated_value"] += animation_info["increment"]

            if animation_info["duration"] is not None:
                animation_info["duration"] -= 1
                return

        animation_info["duration_per_increment_count"] += 1

    def update_increment(self, name: str, increment: Union[int, float], directly_change: bool) -> None:
        if directly_change:
            self._animations[name]["increment"] = increment
        else:
            self._animations[name]["increment"] += increment

        if self._animations[name]["max_increment"] is not None:
            if self._animations[name]["increment"] > self._animations[name]["max_increment"]:
                self._animations[name]["increment"] = self._animations[name]["max_increment"]
            elif self._animations[name]["increment"] < -self._animations[name]["max_increment"]:
                self._animations[name]["increment"] = -self._animations[name]["max_increment"]

    def get_animated_value(self, name: str) -> Union[int, float, bool]:
        return self._animations[name]["animated_value"]