# Habit Tracking App

## Overview
This habit tracking app helps users build and maintain good habits by tracking daily or weekly tasks. Users can create habits, mark them as done, and analyze their progress through a command-line interface (CLI).

## Features
- Create multiple habits with daily or weekly periodicity.
- Mark habits as completed.
- Track streaks of completed habits.
- Analyze habits to see the longest streaks and filter by periodicity.

## Requirements
- Python 3.7 or later
- `click` library
- `sqlite3` library

## Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```bash
    cd path/to/your/project
    ```
3. Install the required libraries:
    ```bash
    pip install click
    ```

## Usage
### Initialize the Database
Before using the app, initialize the database with example data:
```bash
python habit.py initialize
```
Expected Output:
```
Database initialized with example data.
```

### Create a New Habit
Create a new habit with a name, description, and periodicity (daily or weekly):
```bash
python habit.py create-habit "Exercise" "Daily exercise routine" "daily"
```
Expected Output:
```
Habit Exercise created.
```

### Complete a Habit Task
Mark a habit task as completed:
```bash
python habit.py complete-task "Exercise"
```
Expected Output:
```
Habit Exercise marked as completed.
```

### Show All Habits
Display all tracked habits:
```bash
python habit.py show-habits
```
Expected Output:
```
Less Sugar: Consume less sugar daily [daily]
More Water: Drink at least 8 glasses of water [daily]
Eat Vegetables: Include vegetables in meals [daily]
No Junk Food: Avoid junk food [daily]
Grocery Shopping: Do grocery shopping once a week [weekly]
Exercise: Daily exercise routine [daily]
```

### Show Habits by Periodicity
Display habits filtered by periodicity:
```bash
python habit.py show-habits-by-periodicity daily
```
Expected Output:
```
Less Sugar: Consume less sugar daily [daily]
More Water: Drink at least 8 glasses of water [daily]
Eat Vegetables: Include vegetables in meals [daily]
No Junk Food: Avoid junk food [daily]
Exercise: Daily exercise routine [daily]
```

### Show Longest Streaks
Display the longest streaks for all habits:
```bash
python habit.py show-streaks
```
Expected Output:
```
Less Sugar: Longest streak is 28.
More Water: Longest streak is 28.
Eat Vegetables: Longest streak is 28.
No Junk Food: Longest streak is 28.
Grocery Shopping: Longest streak is 4.
Exercise: Longest streak is 1.
```

### Show Longest Run Streak of All Habits
Display the longest run streak of all habits:
```bash
python habit.py show-longest-run-streak
```
Expected Output:
```
Longest run streak of all habits is 28.
```

### Show Longest Streak for a Specific Habit
Display the longest streak for a specific habit:
```bash
python habit.py longest-streak-for-habit "Less Sugar"
```
Expected Output:
```
Longest streak for habit Less Sugar is 28.
```

## Running Tests
Ensure you have `pytest` installed:
```bash
pip install pytest
```
Run the tests:
```bash
pytest test_habit.py
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
