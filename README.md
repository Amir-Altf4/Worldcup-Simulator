# World Cup 2026 Simulator
A Python simulation of the 2026 FIFA World Cup. Runs the full tournament from group stage to final, and can simulate it thousands of times to calculate each team's championship probability.

## Features

- Loads 32 teams from a CSV file
- Seeds and draws groups based on FIFA rankings
- Simulates group stage matches using Poisson distribution
- Runs knockout rounds with extra time and penalty shootouts
- Simulates the tournament a specified number of times and reports championship percentages
- Displays the full knockout bracket
- Visualizes championship probabilities as a bar chart (top 10 teams)

## Requirements

- Python
- numpy
- matplotlib (optional — chart will be skipped if not installed)

Install dependencies:

pip install numpy matplotlib

## Project Structure

worldcup_project/
├── main.py                    # Entry point and menu
├── modules/
│   ├── team.py                # Team class
│   ├── match.py               # Match class
│   ├── group.py               # Group class
│   ├── knockout_stage.py      # KnockoutStage class
│   └── world_cup_simulator.py # WorldCupSimulator class
└── worldcup_2026_teams.txt    # Team data

## How to Run

python main.py

## Menu Options

1. Load teams from CSV
2. Seed and draw groups
3. Run group stage and display standings
4. Run full tournament and display champion
5. Simulate N times and report championship percentages
6. Display knockout bracket from last simulation
7. Exit

## How It Works

Group Stage: Each team plays against every other team in their group once. Teams are ranked by points, goal difference, and goals scored.

Knockout Stage: Matches follow FIFA bracket rules. Draws go to extra time, then penalties if needed.

Simulation: Match scores are generated using a Poisson distribution. The expected number of goals is calculated from each team's attack rating and the opponent's defense rating.

Chart: After running multiple simulations, a horizontal bar chart is generated showing the top 10 teams by championship probability. The chart is also saved as champion_stats.png.

## Author

Amir Bagheri
Computer Engineering Student
