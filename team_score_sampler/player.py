
import numpy as np


class Player:

    def __init__(self, name, pos, mean=0.0, std=1.0) -> None:
        self.name_ = name
        self.pos_ = pos
        self.mean_ = mean
        self.std_ = std
        self.generator_ = np.random.default_rng()

    def update_distribution(self, mean: float, std: float) -> None:
        self.mean_ = mean
        self.std_ = std

    def get_name(self) -> str:
        return self.name_

    def get_position(self) -> str:
        return self.pos_

    def get_mean(self) -> float:
        return self.mean_

    def get_std(self) -> float:
        return self.std_

    def simulate_score(self, n_samples=1) -> float:
        scores = self.generator_.normal(self.mean_, self.std_, n_samples)
        return scores
