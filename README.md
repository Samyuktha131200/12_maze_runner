# Maze Runner

Navigate through a procedurally generated maze to reach the exit using **Pygame**.

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| W / UP | Move up |
| S / DOWN | Move down |
| A / LEFT | Move left |
| D / RIGHT | Move right |
| R | Generate new maze |
| H | Show / hide shortest path hint |

## Tasks to Complete

### Task 1: Shortest Path Hint
> Press H to show the solution path highlighted in the maze.

**Quick Start Prompt:**
```
Add a BFS solver to my pygame maze. When H is pressed, highlight the shortest path from start to exit by drawing colored squares on each cell in the path. Toggle it off on second press.
```

### Task 2: Fog of War
> Only show maze cells within a radius of 3 cells around the player; the rest is dark.

**Quick Start Prompt:**
```
Add fog of war to my maze game. Draw a dark overlay over the whole maze surface, then cut out a circular transparent region around the player using pygame.draw.circle on a surface with SRCALPHA. Reveal only nearby cells.
```

### Task 3: Timer Leaderboard
> Track the top 5 best completion times and display them after solving.

**Quick Start Prompt:**
```
After the player solves the maze, save their time to a list (up to 5 entries, sorted ascending). Display the leaderboard on the win screen. Persist it in a JSON file called leaderboard.json.
```

### Task 4: Larger Maze Difficulty Tiers
> Add Easy (10x8), Medium (15x13), Hard (20x18) options selectable at start.

**Quick Start Prompt:**
```
Add a difficulty select screen before the maze generates. Show three buttons (Easy, Medium, Hard) with different COLS/ROWS values. Let the player click to select, then launch the maze with those dimensions.
```

## Folder Structure

```
maze-runner/
├── main.py
├── requirements.txt
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── maze.py
│   └── player.py
└── README.md
```

## Submission Checklist

- [ ] All 4 tasks completed
- [ ] Maze is generated fresh each session (R key)
- [ ] Fog of war renders correctly
- [ ] Timer leaderboard persists to JSON
- [ ] Code reviewed with LLM (include chat link)
