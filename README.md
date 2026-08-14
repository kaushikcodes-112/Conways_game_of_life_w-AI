# Conway's Game of Life: AI Micro-Intervention

A Python and Pygame implementation of Conway's Game of Life, featuring an AI agent that actively micromanages the grid to prevent cellular extinction. The AI dynamically calculates dying cells and intervenes by flipping states (spawning neighbors or removing overcrowding) based on a configurable budget.

## Features
* **Universal Rule Engine:** Supports any Birth/Survival rule string (e.g., B3/S23, B36/S23).
* **AI Micro-Agent:** Actively fights to keep cells alive without breaking the underlying simulation logic.
* **Interactive Grid:** Draw and erase cells in real-time while the simulation runs.

## Installation

1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/kaushikcodes-112/Conways_game_of_life_w-AI.git)
   cd Conways_game_of_life_w-AI

2. Install the required dependencies (Pygame):
  pip install pygame

4. Run the application:
   python main.py

Configuration Menu
When you launch main.py, a lightweight terminal menu will prompt you to configure the simulation rules before the graphical window opens. Pressing ENTER will default to the standard Conway settings.

Birth Rules: The exact number of neighbors required for a dead cell to become alive. (Default: 3)

Survival Rules: The exact number of neighbors required for a living cell to stay alive. (Default: 23)

AI Toggle Budget: The maximum number of micro-interventions (cell flips) the AI is allowed to make per generation. (Default: 7)

Controls:
The simulation can be fully manipulated at runtime using your keyboard and mouse.
Input                        Action
Mouse Left Click        Manually draw or erase cells on the grid
SPACE                   Play / Pause the simulation 
A                       Toggle the AI Agent ON or OFF
G                       Generate a random cluster of cells
C                       Clear the entire grid
UP Arrow                Increase simulation speed
DOWN Arrow              Decrease simulation speed
