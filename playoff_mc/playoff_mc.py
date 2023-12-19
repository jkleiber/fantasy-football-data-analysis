
import argparse

from tournament import Tournament


if __name__ == "__main__":
    # Parse user arguments
    parser = argparse.ArgumentParser(
        prog="Playoff MC",
        description="Runs a Monte-Carlo for a playoff bracket to determine likelihood of a champion")

    # File defining the playoff structure and teams
    parser.add_argument('file')
    # Number of playoffs to simulate.
    parser.add_argument('--n_runs', default=100000)

    args = parser.parse_args()

    # Turn arguments into local variables.
    tournament_file = args.file
    n_runs = args.n_runs

    # Save the winners.
    winners = {}
    for i in range(n_runs):
        tournament = Tournament(tournament_file, i)

        winner = tournament.run_tournament(False, False)

        win_name = winner.get_name()
        if win_name in winners.keys():
            winners[win_name] += 1 / n_runs
        else:
            winners[win_name] = 1 / n_runs

    print(winners)
