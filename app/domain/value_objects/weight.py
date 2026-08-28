from dataclasses import dataclass


@dataclass(frozen=True)
class Weight:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Weight cannot be negative")
        if self.value > 100:
            raise ValueError("Weight exceeds maximum supported value")