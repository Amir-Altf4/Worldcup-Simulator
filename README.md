# 🌍 World Cup 2026 Simulator

A Python-based simulator for the **2026 FIFA World Cup**. The program simulates the entire tournament—from the group stage to the final—and can run thousands of simulations to estimate each team's probability of becoming world champion.

---

## ✨ Features

- Load all 32 teams from a data file
- Seed teams and randomly draw World Cup groups based on FIFA rankings
- Simulate group stage matches using the **Poisson distribution**
- Simulate knockout rounds, including:
  - Extra Time
  - Penalty Shootouts
- Run the tournament any number of times to calculate championship probabilities
- Display the complete knockout bracket
- Generate and save a horizontal bar chart of the **Top 10 championship probabilities**

---

## 📦 Requirements

- Python 3.8+
- NumPy
- Matplotlib *(optional — the simulator works without it, but charts will be skipped)*

Install the required packages:

```bash
pip install numpy matplotlib
```

---

## 📁 Project Structure

```text
worldcup_project/
│
├── main.py
│
├── modules/
│   ├── team.py
│   ├── match.py
│   ├── group.py
│   ├── knockout_stage.py
│   └── world_cup_simulator.py
│
└── worldcup_2026_teams.txt
```

### File Overview

| File | Description |
|------|-------------|
| `main.py` | Program entry point and interactive menu |
| `team.py` | Team class |
| `match.py` | Match simulation logic |
| `group.py` | Group stage logic |
| `knockout_stage.py` | Knockout bracket management |
| `world_cup_simulator.py` | Main simulator controller |
| `worldcup_2026_teams.txt` | Team data |

---

## 🚀 Running the Project

```bash
python main.py
```

---

## 📋 Menu

```
1. Load teams from file
2. Seed and draw groups
3. Run group stage and display standings
4. Run full tournament and display champion
5. Simulate N tournaments and report championship probabilities
6. Display knockout bracket from the last simulation
7. Exit
```

---

## ⚙️ Simulation Model

### Group Stage

Each team plays every other team in its group once.

Teams are ranked by:

1. Points
2. Goal Difference
3. Goals Scored

---

### Knockout Stage

Every knockout match follows FIFA rules:

- 90 minutes
- Extra Time (if tied)
- Penalty Shootout (if still tied)

---

### Match Simulation

Match scores are generated using a **Poisson distribution**.

Expected goals are calculated from:

- Team attacking strength
- Opponent defensive strength

This creates realistic score distributions while preserving stronger teams' higher chances of winning.

---

### Championship Simulation

The simulator can run the tournament thousands of times.

After all simulations, it reports each team's probability of winning the World Cup.

If **Matplotlib** is installed, it also:

- Displays a horizontal bar chart of the **Top 10 teams**
- Saves the chart as:

```text
champion_stats.png
```

---

## 👨‍💻 Author

**Amir Bagheri**

Computer Engineering Student
