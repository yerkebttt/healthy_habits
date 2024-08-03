import sqlite3
from datetime import datetime, timedelta
import click

DATABASE = 'habits.db'

class Habit:
    def __init__(self, name, description, periodicity):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created_at = datetime.now()
        self.check_dates = []

    def check(self, date=None):
        if date is None:
            date = datetime.now()
        self.check_dates.append(date)

    def compute_streak(self):
        sorted_dates = sorted(set(d.date() for d in self.check_dates))
        if not sorted_dates:
            return 0
        
        longest_streak = 0
        current_streak = 1
        interval = timedelta(days=1) if self.periodicity == 'daily' else timedelta(weeks=1)

        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] - sorted_dates[i-1] <= interval:
                current_streak += 1
            else:
                current_streak = 1

            longest_streak = max(longest_streak, current_streak)

        return longest_streak

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'periodicity': self.periodicity,
            'created_at': self.created_at.isoformat(),
            'check_dates': [date.isoformat() for date in self.check_dates]
        }

    @classmethod
    def from_dict(cls, data):
        habit = cls(data['name'], data['description'], data['periodicity'])
        habit.created_at = datetime.fromisoformat(data['created_at'])
        habit.check_dates = [datetime.fromisoformat(date) if isinstance(date, str) else date for date in data.get('check_dates', [])]
        return habit

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS habits (
                                    name TEXT PRIMARY KEY,
                                    description TEXT,
                                    periodicity TEXT,
                                    created_at TEXT
                                 )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS habit_checks (
                                    habit_name TEXT,
                                    check_date TEXT,
                                    FOREIGN KEY(habit_name) REFERENCES habits(name)
                                 )''')

    def add_habit(self, habit):
        with self.conn:
            self.conn.execute('''INSERT INTO habits (name, description, periodicity, created_at)
                                 VALUES (?, ?, ?, ?)''', (habit.name, habit.description, habit.periodicity, habit.created_at.isoformat()))

    def complete_task(self, habit_name, date=None):
        if date is None:
            date = datetime.now()
        with self.conn:
            self.conn.execute('''INSERT INTO habit_checks (habit_name, check_date)
                                 VALUES (?, ?)''', (habit_name, date.isoformat()))

    def get_habits(self):
        with self.conn:
            habits = self.conn.execute('''SELECT * FROM habits''').fetchall()
            return [Habit.from_dict({
                'name': row[0],
                'description': row[1],
                'periodicity': row[2],
                'created_at': row[3],
                'check_dates': self.get_check_dates(row[0])
            }) for row in habits]

    def get_check_dates(self, habit_name):
        with self.conn:
            checks = self.conn.execute('''SELECT check_date FROM habit_checks WHERE habit_name = ?''', (habit_name,)).fetchall()
            return [datetime.fromisoformat(row[0]) for row in checks]

    def clear_database(self):
        with self.conn:
            self.conn.execute('DELETE FROM habit_checks')
            self.conn.execute('DELETE FROM habits')

    def initialize_with_example_data(self):
        self.clear_database()

        # Predefined habits
        predefined_habits = [
            Habit("Less Sugar", "Consume less sugar daily", "daily"),
            Habit("More Water", "Drink at least 8 glasses of water", "daily"),
            Habit("Eat Vegetables", "Include vegetables in meals", "daily"),
            Habit("No Junk Food", "Avoid junk food", "daily"),
            Habit("Grocery Shopping", "Do grocery shopping once a week", "weekly")
        ]

        # Add habits to the database
        for habit in predefined_habits:
            self.add_habit(habit)

        # Example tracking data for 4 weeks
        for habit in predefined_habits:
            if habit.periodicity == "daily":
                dates = [datetime.now() - timedelta(days=i) for i in range(28)]
            else:
                dates = [datetime.now() - timedelta(weeks=i) for i in range(4)]

            for date in dates:
                self.complete_task(habit.name, date)

# Analytics functions using functional programming paradigm
def list_all_habits(database):
    return database.get_habits()

def list_habits_by_periodicity(database, periodicity):
    return [habit for habit in database.get_habits() if habit.periodicity == periodicity]

def longest_run_streak_all_habits(database):
    return max((habit.compute_streak() for habit in database.get_habits()), default=0)

def longest_run_streak_for_habit(database, habit_name):
    habits = database.get_habits()
    for habit in habits:
        if habit.name == habit_name:
            return habit.compute_streak()
    return 0

@click.group()
def cli():
    pass

@click.command()
@click.argument('name')
@click.argument('description')
@click.argument('periodicity')
def create_habit(name, description, periodicity):
    """Create a new habit"""
    db = Database()
    habit = Habit(name, description, periodicity)
    db.add_habit(habit)
    click.echo(f'Habit {name} created.')

@click.command()
@click.argument('name')
def complete_task(name):
    """Mark a habit task as completed"""
    db = Database()
    db.complete_task(name)
    click.echo(f'Habit {name} marked as completed.')

@click.command()
def show_habits():
    """Show all habits"""
    db = Database()
    habits = list_all_habits(db)
    for habit in habits:
        click.echo(f'{habit.name}: {habit.description} [{habit.periodicity}]')

@click.command()
@click.argument('periodicity')
def show_habits_by_periodicity(periodicity):
    """Show habits by periodicity"""
    db = Database()
    habits = list_habits_by_periodicity(db, periodicity)
    for habit in habits:
        click.echo(f'{habit.name}: {habit.description} [{habit.periodicity}]')

@click.command()
def show_streaks():
    """Show longest streaks"""
    db = Database()
    habits = list_all_habits(db)
    for habit in habits:
        streak = habit.compute_streak()
        click.echo(f'{habit.name}: Longest streak is {streak}.')

@click.command()
def show_longest_run_streak():
    """Show the longest run streak of all habits"""
    db = Database()
    streak = longest_run_streak_all_habits(db)
    click.echo(f'Longest run streak of all habits is {streak}.')

@click.command()
@click.argument('name')
def longest_streak_for_habit(name):
    """Show the longest streak for a specific habit"""
    db = Database()
    streak = longest_run_streak_for_habit(db, name)
    click.echo(f'Longest streak for habit {name} is {streak}.')

@click.command()
def initialize():
    """Initialize the database with example data"""
    db = Database()
    db.initialize_with_example_data()
    click.echo('Database initialized with example data.')

cli.add_command(create_habit)
cli.add_command(complete_task)
cli.add_command(show_habits)
cli.add_command(show_habits_by_periodicity)
cli.add_command(show_streaks)
cli.add_command(show_longest_run_streak)
cli.add_command(longest_streak_for_habit)
cli.add_command(initialize)

if __name__ == '__main__':
    cli()
