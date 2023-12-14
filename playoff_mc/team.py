
import numpy as np

class Team:
    def __init__(self, name, rank, mean=0.0, std=1.0) -> None:
        self.name_ = name
        self.rank_ = rank
        self.mean_ = mean
        self.std_ = std
        self.generator_ = np.random.default_rng()

    def update_distribution(self, mean: float, std: float) -> None:
        self.mean_ = mean
        self.std_ = std

    def get_name(self) -> str:
        return self.name_

    def simulate_score(self, n_samples=1) -> float:
        scores = self.generator_.normal(self.mean_, self.std_, n_samples)
        return scores
