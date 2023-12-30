
import argparse
import json
import numpy as np

from matplotlib import pyplot as plt

from roster import Roster


def normal_dist(x, mean: float, std_dev: float):
    pdf = np.exp(-0.5*((x - mean) / std_dev)**2) / (std_dev * np.sqrt(2.0*np.pi))
    return pdf


if __name__ == "__main__":
    # Parse user arguments
    parser = argparse.ArgumentParser(
        prog="FF Team MC",
        description="Runs a Monte-Carlo for a fantasy football team to determine possible score distribution")

    # File defining the available players and roster to simulate
    parser.add_argument('roster_file')
    parser.add_argument('players_file')
    # Number of games to simulate.
    parser.add_argument('--n_runs', default=10000)

    args = parser.parse_args()

    # Turn arguments into local variables.
    roster_file = args.roster_file
    player_file = args.players_file
    n_runs = args.n_runs

    # Create a dictionary of player data from the player file.
    player_dict = {}
    with open(player_file, 'r') as f:
        player_info = json.load(f)

        for player in player_info['players']:
            player_dict[player['name']] = player

    # Get the roster.
    roster = Roster(roster_file, player_dict)

    # Save the scores.
    scores = roster.simulate_score(n_samples=n_runs)

    print("ROSTER:")
    print(roster)

    # Statistics
    scores = np.array(scores)
    min_score = np.min(scores)
    max_score = np.max(scores)
    mean_score = np.mean(scores)
    std_dev = np.std(scores)

    print("RESULTS")
    print(
        f"Average score: {mean_score:.2f} | Std: {std_dev:.2f} | Range: [{min_score:.2f}, {max_score:.2f}] | 1-sigma range: [{(mean_score-std_dev):.2f}, {(mean_score+std_dev):.2f}]")

    plt.figure()

    bins = np.linspace(min_score - 10, max_score + 10, 20)
    hist, edges = np.histogram(scores, density=True, bins=bins)

    x = np.linspace(min_score - 10, max_score + 10, 1000)
    pdf = normal_dist(x, mean_score, std_dev)

    one_std_prob = normal_dist(mean_score + std_dev, mean_score, std_dev)

    plt.plot(x, pdf, color='k')
    plt.hist(scores, bins=20, color='skyblue', histtype='bar', rwidth=0.8, density=True)
    plt.vlines(mean_score + std_dev, ymin=0, ymax=one_std_prob, color='r', linestyle='--')
    plt.vlines(mean_score - std_dev, ymin=0, ymax=one_std_prob, color='r', linestyle='--')

    plt.suptitle("Team Score Distribution")
    plt.title(
        f"Average score: {mean_score:.2f} | Std: {std_dev:.2f} | Range: [{min_score:.2f}, {max_score:.2f}] | 1-sigma range: [{(mean_score-std_dev):.2f}, {(mean_score+std_dev):.2f}]", size=8, wrap=True)
    plt.ylabel("Number of Occurences")
    plt.xlabel("Scores")

    plt.show(block=False)

    input("[press enter to exit]")
