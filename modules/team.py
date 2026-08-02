import numpy as np
import random


class Team:
    """Represents a football team in the World Cup simulator.

    This class stores the team's attributes (name, attack, defense, rank)
    and match statistics (goals for, goals against, points, group), and
    implements the logic to simulate a match.
    """

    def __init__(self, name, attack, defense, rank):
        """Create a new team with basic attributes.

        Args:
            name (str): Team name.
            attack (int): Attack strength (0-100).
            defense (int): Defense strength (0-100).
            rank (int): World ranking used for seeding.
        """
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank
        # Initial statistics are zero
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = None
        
    def goal_difference(self):
        """Calculate the team's goal difference.

        Returns:
            int: Goal difference.
        """
        return self.goals_for - self.goals_against   
     
    def reset_stats(self):
        """Reset the team's match statistics for a fresh simulation run."""
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
    
    def simulate_match(self, opponent, is_knockout = False):
        """Simulate a match against an opponent.

        In the group stage only 90 minutes are played. In knockout rounds,
        if tied, extra time and, if needed, penalties are simulated.

        Args:
            opponent (Team): Opposing team.
            is_knockout (bool): If True, knockout rules (extra time and
                penalties) apply.

        Returns:
            tuple: (team_goals, opponent_goals, winner). In the group stage
                a draw returns winner as None.
        """
        
        # Simulate the 90-minute match result
        goals_self, goals_opp = self._play_90_minutes(opponent)
        # Draws are allowed in the group stage
        if not is_knockout: 
            winner = None
            if goals_self > goals_opp:
             winner = self
            elif goals_opp > goals_self:
             winner = opponent
            return goals_self, goals_opp, winner

        # In knockout stage, if tied, play extra time
        if goals_self == goals_opp:
         et_self, et_opp = self._play_extra_time(opponent)
         goals_self += et_self
         goals_opp += et_opp
        # If still tied, go to penalties
        if goals_self == goals_opp:
            pen_self, pen_opp, winner = self._play_penalties(opponent)
        # Penalty goals are not added to the match goal totals
            return goals_self, goals_opp, winner

        winner = self if goals_self > goals_opp else opponent
        return goals_self, goals_opp, winner
    
    def _play_90_minutes(self, opponent):
        """
        Simulate 90 minutes using a Poisson distribution.
 
        Returns:
            tuple: (team_goals, opponent_goals)
        """
        # Expected mean goals.
        # Higher attack and weaker opponent defense increase scoring chance.
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8
        
        # Generate goal counts using a Poisson distribution
        goals_self = np.random.poisson(lambda_self)
        goals_opp = np.random.poisson(lambda_opponent)
        return goals_self, goals_opp
    
    def _play_extra_time(self, opponent):
        """
        Simulate 30 minutes of extra time.
 
        Returns:
            tuple: (team_goals, opponent_goals) in extra time
        """
        # Because it's 30 minutes, scale the mean by ~0.33
        lambda_self = ((self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8) * 0.33
        lambda_opponent = ((opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8) * 0.33
        # Poisson distribution samples random counts based on the lambda
        goals_self = np.random.poisson(lambda_self)
        goals_opp = np.random.poisson (lambda_opponent)
        
        return goals_self, goals_opp
    
    def _play_penalties(self, opponent):
        """
        Simulate a penalty shootout: first 5 kicks each, then sudden death.
 
        Returns:
            tuple: (team_score, opponent_score, winner)
        """


        def take_penalty(attacker, defender):
            """Simulate a single penalty kick."""
            # Compute scoring probability based on attack and defense
            P = 0.75 + (attacker.attack - defender.defense) / 250
            # Clamp probability between 60% and 90%
            P = max(0.6, min(0.9, P))
            # Determine if the kick is scored
            return random.random() < P
        
        # Count first team's goals in the initial five penalties
        score_self = 0
        for _ in range(5):
            if take_penalty(self, opponent):
                score_self += 1
                
        # Count second team's goals in the initial five penalties
        score_opponent = 0
        for _ in range(5):
            if take_penalty(opponent, self):
                score_opponent += 1
                
        # Execute sudden-death penalties until a winner is decided
        while score_self == score_opponent:
            if take_penalty(self, opponent):
                score_self += 1
            if take_penalty(opponent, self):
                score_opponent += 1
            if score_self != score_opponent:
                break
            
        # Determine the penalty shootout winner
        winner = self if score_self > score_opponent else opponent

        return score_self, score_opponent, winner