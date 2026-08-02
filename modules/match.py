class Match:
    """Represents a match between two teams.

    This class links two teams, runs the match simulation,
    and records the result in the teams' statistics.
    """

    def __init__(self, team1, team2, is_knockout = False):
        """Create a new match between two teams.

        Args:
            team1 (Team): First team.
            team2 (Team): Second team.
            is_knockout (bool): If True, the match is played under
                knockout rules.
        """
        self.team1 = team1
        self.team2 = team2

        # Mark whether the match is group-stage or knockout
        self.is_knockout = is_knockout
        self.goals1 = 0
        self.goals2 = 0
        self.winner = None

    def play(self):
        """Play the match and update both teams' statistics.

        Simulates the match result, adds goals and points (in group stage)
        to each team's stats.

        Returns:
            None
        """
        # Simulate the match and get the result
        self.goals1, self.goals2, self.winner = self.team1.simulate_match(self.team2, self.is_knockout)

        # Update goals statistics for both teams
        self.team1.goals_for += self.goals1
        self.team2.goals_for += self.goals2
        self.team1.goals_against += self.goals2
        self.team2.goals_against += self.goals1

        # Points are only awarded in the group stage — knockout has no points
        if not self.is_knockout:
            # First team win
            if self.goals1 > self.goals2:
                self.team1.points += 3
            # Second team win
            elif self.goals2 > self.goals1:
                self.team2.points += 3
            # Draw; each team receives one point
            else:
                self.team1.points += 1
                self.team2.points += 1