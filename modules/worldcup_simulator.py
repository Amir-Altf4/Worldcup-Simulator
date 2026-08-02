import csv
import random

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

from modules.group import Group
from modules.knockout_stage import KnockoutStage
from modules.match import Match
from modules.team import Team


class WorldCupSimulator:
    """Full tournament World Cup simulator.

    This class coordinates loading teams, drawing groups, running the group
    stage and knockout stage, and statistical analysis of championship
    probabilities.
    """

    def __init__(self):
        """Create a new simulator with empty initial state."""
        self.teams = []
        self.groups = []
        # These rounds are initially None and will be populated later.
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None
        
    def load_teams_from_csv(self, filename):
        """Load teams from a CSV file.

        Args:
            filename (str): The CSV filename.
        """
        # Ensure the teams list is empty for each run.
        self.teams = []
        try:
            with open(filename) as f:
               reader = csv.DictReader(f)
               for row in reader:
                   new_team = Team((row["name"]), int(row["attack"]), int(row["defense"]), int(row["rank"]))
                   self.teams.append(new_team)
        except FileNotFoundError:
            print("File not found!")
            
          
    def seed_and_draw(self):
        """Seed teams by ranking and draw them into groups."""
        # Reset groups because this may be called many times (e.g., 1000 sims)
        self.groups = []
        # Sort teams by world ranking
        self.teams.sort(key=lambda t: t.rank)
        # Split into 4 seed pots of 8 teams based on rank
        seed1 = self.teams[0:8]
        seed2 = self.teams[8:16]
        seed3 = self.teams[16:24]
        seed4 = self.teams[24:32]

        group_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        # Create 8 empty groups
        for i in range(8):
            group_name = group_names[i]
            self.groups.append(Group(group_name, []))
        # Draw each seed pot separately
        for seed in [seed1, seed2, seed3, seed4]:
            random.shuffle(seed)
            # Assign each team to one of the groups
            for i, team in enumerate(seed):
                # Register the group's name on the team
                team.group = self.groups[i].name
                # Add the team to the corresponding group
                self.groups[i].teams.append(team)
         
    def run_group_stage(self, show_table=True):
        """Run the group stage and optionally display results."""
        for group in self.groups:
            group.play_all_matches()
            
            # Optionally display the group's table
            if show_table:
                
              print(f"=== {group.name} ===")
              ranking = group.get_ranking()
              for i, team in enumerate(ranking):
                  print(f"{i+1}. {team.name}: {team.points} points GD {team.goal_difference()} GF {team.goals_for}")
                
    def setup_knockout_bracket(self):
        """Create the knockout bracket from group stage results."""
        results = {}
        # Determine first and second place for each group
        for group in self.groups:
            first, second = group.advance_teams()
            results[group.name] = (first, second)
        # Build the 8 round-of-16 matches
        match_r16 = [
            # First of Group A vs Second of Group B
            Match(results["A"][0], results["B"][1], is_knockout=True),
            # First of Group C vs Second of Group D
            Match(results["C"][0], results["D"][1], is_knockout=True),
            # First of Group E vs Second of Group F
            Match(results["E"][0], results["F"][1], is_knockout=True),
            # First of Group G vs Second of Group H
            Match(results["G"][0], results["H"][1], is_knockout=True),
            # First of Group B vs Second of Group A
            Match(results["B"][0], results["A"][1], is_knockout=True),
            # First of Group D vs Second of Group C
            Match(results["D"][0], results["C"][1], is_knockout=True),
            # First of Group F vs Second of Group E
            Match(results["F"][0], results["E"][1], is_knockout=True),
            # First of Group H vs Second of Group G
            Match(results["H"][0], results["G"][1], is_knockout=True),
        ]

        self.round_of_16 = KnockoutStage(match_r16, "round of 16")
    
    def run_knockout_stage(self):
        """Run all knockout rounds and determine the tournament champion."""
    
        self.round_of_16.play_round()
        # Get the teams advancing to the quarterfinals
        winners_r16 = self.round_of_16.get_winners()
        # Build 4 quarterfinal matches
        match_qf = [
            Match(winners_r16[0], winners_r16[1], is_knockout=True),
            Match(winners_r16[2], winners_r16[3], is_knockout=True),
            Match(winners_r16[4], winners_r16[5], is_knockout=True),
            Match(winners_r16[6], winners_r16[7], is_knockout=True),
        ]
        # Create and run the quarterfinals
        self.quarterfinals = KnockoutStage(match_qf, "Quarterfinals")
        self.quarterfinals.play_round()
        winners_qf = self.quarterfinals.get_winners()
        # Build the semifinal matches
        match_sf = [
            Match(winners_qf[0], winners_qf[1], is_knockout=True),
            Match(winners_qf[2], winners_qf[3], is_knockout=True),
        ]
        # Create and run the semifinals
        self.semifinals = KnockoutStage(match_sf, "Semifinals")
        self.semifinals.play_round()
        # Get teams advancing to the final
        winners_sf = self.semifinals.get_winners()
        # Build the final match
        match_f = [Match(winners_sf[0], winners_sf[1], is_knockout=True)]
        # Create and run the final match
        self.final = KnockoutStage(match_f, "Final")
        self.final.play_round()
    
        self.champion = self.final.get_winners()[0]
     
    def run_full_simulation(self):
        """Simulate the entire tournament and return the champion's name."""

        # Reset statistics for all teams
        for team in self.teams:
            team.reset_stats()
        # Draw groups
        self.seed_and_draw()
        # Run group stage
        # show_table=False because in 1000-run simulations there is no need to display tables
        self.run_group_stage(show_table=True)
        # Setup knockout bracket
        self.setup_knockout_bracket()
        # Run knockout stage
        self.run_knockout_stage()
        # Champion
        return self.champion.name
        
    def most_likely_champion(self, num_simulations=1000):
        """Run the group and knockout stages multiple times and report results.

        Args:
            num_simulations (int): Number of simulation runs.
        """
        # Build a dictionary to store team names and their win counts
        champions = {}
        # Run the simulations
        for _ in range(num_simulations):
            # Increase the championship count for the winning team
            name = self.run_full_simulation()
            champions[name] = champions.get(name, 0) + 1
        # Display championship percentages for each team
        print(f"\nResults of {num_simulations} simulations:")
        for name, count in sorted(champions.items(), key=lambda x: x[1], reverse=True):
            print(f"{name}: {count/num_simulations*100:.1f}%")
        
        # Chart plotting is handled separately by the caller
        return champions
    
    def plot_champion_stats(self, champions, num_simulations):
        """Plot championship probability bars based on simulation results.

        Sorts teams by number of championships, computes each team's
        championship probability, and displays a horizontal bar chart of the
        top 10 teams.

        Args:
            champions (dict):
                Dictionary mapping team names to their championship counts.
            num_simulations (int):
                Total number of simulation runs.

        Returns:
            None: Saves the chart to `champion_stats.png` and displays it.
        """
        if plt is None:
            print("matplotlib is not installed")
            return

        # Sort from most to least
        sorted_champions = sorted(champions.items(), key=lambda x: x[1], reverse=True)
        # Only top 10 teams
        names = [item[0] for item in sorted_champions[:10]]
        # Convert championship counts to probabilities (percent)
        percentages = [item[1] / num_simulations * 100 for item in sorted_champions[:10]]
        # Coloring — gold first, silver second, bronze third, blue for others
        colors = []
        for i in range(len(names)):
            if i == 0:
                colors.append('#FFD700')
            elif i == 1:
                colors.append('#C0C0C0')
            elif i == 2:
                colors.append('#CD7F32')
            else:
                colors.append('#4a90d9')

        # Create a plotting figure
        fig, ax = plt.subplots(figsize=(10, 7))
        # names[::-1] reverses the team list
        # percentages[::-1] reverses the percentages accordingly
        bars = ax.barh(names[::-1], percentages[::-1], color=colors[::-1], edgecolor='white')

        # Write the percentage next to each bar
        for bar, pct in zip(bars, percentages[::-1]):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                    f'{pct:.1f}%', va='center', fontsize=10, fontweight='bold')

        # Horizontal axis label
        ax.set_xlabel('Championship Probability (%)')
        # Chart title
        ax.set_title(f'World Cup 2026 — Championship Probability ({num_simulations} Simulations)')
        # Hide top spine of the chart
        ax.spines['top'].set_visible(False)
        # Hide right spine of the chart
        ax.spines['right'].set_visible(False)
        # Add vertical grid lines for better readability of percentages
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        # Adjust layout so labels are not cut off
        plt.tight_layout()
        # Save the chart as a PNG file
        plt.savefig('champion_stats.png', dpi=150, bbox_inches='tight')
        # Show the chart without blocking program execution (block=False)
        plt.show(block=False)
        # Pause briefly to allow the chart to render
        plt.pause(0.1)
     
    def display_bracket(self):
        """Display the knockout stage results (bracket)."""
        # Display results
        print("=== Knockout Bracket ===")
        self.round_of_16.display_results()
        self.quarterfinals.display_results()
        self.semifinals.display_results()
        self.final.display_results()
        print(f"=== Champion : {self.champion.name}")
