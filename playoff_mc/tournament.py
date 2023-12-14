
import json
import copy

from team import Team


class Tournament:

    def __init__(self, file, id) -> None:
        # The tournament is defined as a JSON.
        with open(file, 'r') as f:
            tournament_json = json.load(f)

        # Save this tournament's ID for saving the data later.
        self.id_ = id

        # Store the winner.
        self.winner_ = None

        # Parse the teams into a map.
        self.team_map_ = {}
        self.n_teams_ = len(tournament_json['teams'])
        for i in range(self.n_teams_):
            team_info = tournament_json['teams'][i]

            # Extract team information
            team_name = team_info['name']
            rank = team_info['rank']
            mean = team_info['mean']
            std = team_info['std']

            # Create a team
            team = Team(team_name, rank, mean, std)

            # Save the team in the team map
            self.team_map_[team_name] = team

        # Parse the games into a map.
        # NOTE: it is assumed that all games are played in order from the games list.
        self.schedule_ = {}
        self.n_games_ = len(tournament_json['games'])
        for i in range(self.n_games_):
            game_info = tournament_json['games'][i]

            # Extract game information
            game_name = game_info['name']
            teams = game_info['teams']
            winner_game = game_info['win_game']
            loser_game = game_info['lose_game']

            # Find teams.
            # NOTE: 1v1 is all that is supported at the moment.
            team_1 = None
            team_2 = None
            if len(teams) > 0:
                team_1 = self.team_map_[teams[0]]
            if len(teams) > 1:
                team_2 = self.team_map_[teams[1]]

            # Save the game in the schedule.
            self.schedule_[game_name] = {
                'team_1': team_1,
                'team_2': team_2,
                'win_game': winner_game,
                'lose_game': loser_game
            }

    def run_tournament(self, save_results=True, verbose=True):
        # Play each game.
        for name, game in self.schedule_.items():
            team_1 = game['team_1']
            team_2 = game['team_2']

            winner_next_game = game['win_game']
            loser_next_game = game['lose_game']

            # NOTE: team 1 must exist

            # If Team 2 does not exist, advance Team 1 to the next round.
            if team_2 is None:
                # Print the game results.
                if verbose:
                    print(f"{name} - {team_1.get_name()} advances on BYE.")


                self.advance_team(team_1, winner_next_game)
            else:
                # Otherwise simulate a game.
                t1_score = team_1.simulate_score()
                t2_score = team_2.simulate_score()

                # Save the scores.
                self.schedule_[name]['team_1_score'] = t1_score
                self.schedule_[name]['team_1_score'] = t2_score

                # Print the game results.
                if verbose:
                    print(f"{name} - {team_1.get_name()} {t1_score} - {t2_score} {team_2.get_name()}")

                

                # If team 2 wins outright, advance them as the winner and team 1 as the loser.
                if t2_score > t1_score:
                    self.advance_team(team_1, loser_next_game)
                    self.advance_team(team_2, winner_next_game)

                    # Save the winner if this is the final.
                    if name == "F":
                        self.winner_ = team_2

                else:
                    # Otherwise do the opposite. This auto-advances team 1 in a tie, and team 1 is assumed to be the higher ranked team at the moment.
                    # TODO: decide based on rank or simulate again.
                    self.advance_team(team_1, winner_next_game)
                    self.advance_team(team_2, loser_next_game)

                    # Save the winner if this is the final.
                    if name == "F":
                        self.winner_ = team_1

        if save_results:
            print("Saving results...")
            with open(f"results/tournament_{self.id_}.json", "w") as f:
                json.dump(self.schedule_, f)
        
        # Return the winner of the championship game.
        return self.winner_



    def advance_team(self, team: Team, next_game: str):
        # If there isn't a next game, don't do anything.
        if next_game is None:
            return

        # Get the game the team is advancing to next.
        game = self.schedule_[next_game]

        # If the game already has 2 teams, raise an exception.
        if game['team_1'] is not None and game['team_2'] is not None:
            raise

        # Put this team in the team 1 spot if it is available.
        if game['team_1'] is None:
            self.schedule_[next_game]['team_1'] = team
        else:
            # otherwise put them in the team 2 spot.
            self.schedule_[next_game]['team_2'] = team

