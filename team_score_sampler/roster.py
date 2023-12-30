
import numpy as np
import json

from player import Player


class Roster:

    def __init__(self, team_file: str, player_dict: dict) -> None:
        """
        Arguments:
        - `team_file` (str): path to the roster JSON
        - `player_dict` (dict): dictionary of the player info (statistical distributions, positions, etc.)
        """
        self.players = []

        # Load the roster information.
        roster_info = {}
        with open(team_file, "r") as f:
            roster_info = json.load(f)

        # Associate the players based on name.
        for player in roster_info['roster']:
            player_name = player['name']
            player_info = player_dict[player_name]
            p = Player(player_name, player_info['pos'], player_info['mean'], player_info['std'])

            self.players.append(p)

    def simulate_score(self, n_samples=1) -> float:
        scores = []
        for i in range(n_samples):
            score = 0.0
            for p in self.players:
                score += p.simulate_score()

            scores.append(score)
        return scores

    def __str__(self) -> str:
        team_str = ""
        for p in self.players:
            team_str += f"{p.get_position()}: {p.get_name()} - ({p.get_mean()}, {p.get_std()})\n"

        return team_str
