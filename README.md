# AI Robot Rescue — Run, Learn, Survive

A 2D endless-runner game built with **Python and Pygame**.

## Features
- Three-lane endless runner
- Robot character, jumping and sliding
- Barriers to avoid and energy cells to collect
- AI and cybersecurity quiz checkpoints
- Score, energy count, increasing speed, and saved best score

## Requirements
- Python 3.10 or newer
- Internet connection for the first-time Pygame installation

## Run on Windows
1. Install Python from https://www.python.org/downloads/ (select **Add Python to PATH** during installation).
2. Extract this ZIP file.
3. Open the extracted `AI-Robot-Rescue-Python` folder.
4. Click the folder address bar in File Explorer, type `cmd`, and press Enter.
5. Run:

   ```bash
   py -m pip install -r requirements.txt
   py main.py
   ```

   If `py` does not work, try `python` instead of `py`.

## Controls
- **Left / Right arrow**: change lane
- **Up arrow or Space**: jump over red barriers
- **Down arrow**: slide under purple gates
- **1, 2, 3**: answer a quiz question
- **Enter**: start or restart
- **Esc**: quit

## Notes
- `best_score.json` is created automatically to store the best score.
- The game is a 2D prototype. It does not need Java, Spring Boot, a database, or a web server.
