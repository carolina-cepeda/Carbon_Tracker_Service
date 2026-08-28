from dataclasses import dataclass


@dataclass(frozen=True)
class Distance:
    value: float

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("Distance must be greater than zero")
        if self.value > 100_000:
            raise ValueError("Distance exceeds maximum supported value")