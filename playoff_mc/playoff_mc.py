
from tournament import Tournament

n_runs = 10000

if __name__ == "__main__":
   

    # Save the winners.
    winners = {}
    for i in range(n_runs):
        tournament = Tournament("data/tournament.json", i)

        winner = tournament.run_tournament(False, False)
        
        win_name = winner.get_name()
        if win_name in winners.keys():
            winners[win_name] += 1
        else:
            winners[win_name] = 1
    
    print(winners)
