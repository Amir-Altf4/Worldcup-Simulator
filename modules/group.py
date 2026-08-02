import random
from modules.match import Match

class Group:
    """Represents a group in the World Cup group stage.

    This class manages the teams in a group, runs the round-robin
    matches for the group, and computes the ranking.
    """

    def __init__(self, name, teams):
        """Create a new group with a name and list of teams.

        Args:
            name (str): Group name (e.g., "A").
            teams (list[Team]): List of teams in this group.
        """
        self.name = name
        self.teams = teams
        
    def play_all_matches(self):
        """Play all round-robin matches between teams in the group.

        Each team plays once against every other team in the group.

        Returns:
            None
        """
        
        # Iterate over all teams in the group
        for i in range(len(self.teams)):
            # j starts from i+1 to avoid duplicate matches
            for j in range(i + 1, len(self.teams)):
                
                # Create a match between the two teams
                match = Match(self.teams[i], self.teams[j])
                match.play()
    
    def get_ranking(self):
        """Sort the group's teams by points and tie-break criteria.

        Tie-break criteria in order: points, goal difference, goals scored,
        and random choice as a final tie-break.

        Returns:
            list[Team]: Teams sorted in descending order.
        """
        
        # Sort teams according to ranking criteria
        self.teams.sort(
        key = lambda t: (t.points, t.goal_difference(), t.goals_for, random.random()),
        reverse = True    
        )
        # Return the final group table
        return self.teams
    
    def advance_teams(self):
        """Return the top two teams from the group for the knockout stage.

        Returns:
            list[Team]: The top two teams in the group's ranking.
        """
        
        # Get the ranking table
        ranking = self.get_ranking()
        
        # Return the top two teams
        return ranking[:2]