class KnockoutStage:
    """Represents a knockout round in the World Cup.

    This class manages a collection of knockout matches for a single round
    (e.g., Round of 16, Final) and displays their results.
    """

    def __init__(self, matches, round_name):
        """Create a new knockout round.

        Args:
            matches (list[Match]): List of matches for this round.
            round_name (str): Round name (e.g., "Quarterfinals").
        """
        self.matches = matches
        self.round_name = round_name
    
    def play_round(self):
        """Play all matches in this knockout round."""
        # Run all matches in this round
        for match in self.matches:
            match.play()
            
    def get_winners(self):
        """Return the winners of all matches in this round.

        Returns:
            list[Team]: List of winning teams in match order.
        """
        winners = []
        for match in self.matches:
            winners.append(match.winner)
        return winners
    
    def display_results(self):
        """Print the results of matches in this round."""
        print(f"==={self.round_name}===")
        for match in self.matches:
            # If the first team won
            if match.team1 == match.winner:
                print(f"{match.winner.name} {match.goals1} , {match.goals2} {match.team2.name} => winner: {match.winner.name}")
            # If the second team won
            elif match.team2 == match.winner:
                print(f"{match.winner.name} {match.goals2} , {match.goals1} {match.team1.name} => winner: {match.winner.name}")
