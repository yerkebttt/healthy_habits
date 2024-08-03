import unittest
from datetime import datetime, timedelta
from habit import Habit, Database

class TestHabit(unittest.TestCase):

    def test_create_habit(self):
        habit = Habit("Test Habit", "This is a test habit", "daily")
        self.assertEqual(habit.name, "Test Habit")
        self.assertEqual(habit.description, "This is a test habit")
        self.assertEqual(habit.periodicity, "daily")

    def test_habit_check(self):
        habit = Habit("Test Habit", "This is a test habit", "daily")
        habit.check()
        self.assertEqual(len(habit.check_dates), 1)
        self.assertEqual(habit.check_dates[0].date(), datetime.now().date())

    def test_habit_streak(self):
        habit = Habit("Test Habit", "This is a test habit", "daily")
        habit.check(datetime.now() - timedelta(days=1))
        habit.check(datetime.now())
        self.assertEqual(habit.compute_streak(), 2)

    def test_database_add_habit(self):
        db = Database()
        db.clear_database()
        habit = Habit("Test Habit", "This is a test habit", "daily")
        db.add_habit(habit)
        habits = db.get_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0].name, "Test Habit")

    def test_database_complete_task(self):
        db = Database()
        db.clear_database()
        habit = Habit("Test Habit", "This is a test habit", "daily")
        db.add_habit(habit)
        db.complete_task("Test Habit")
        habits = db.get_habits()
        self.assertEqual(len(habits[0].check_dates), 1)

    def test_list_all_habits(self):
        db = Database()
        db.clear_database()
        habit1 = Habit("Habit 1", "Description 1", "daily")
        habit2 = Habit("Habit 2", "Description 2", "weekly")
        db.add_habit(habit1)
        db.add_habit(habit2)
        habits = db.get_habits()
        self.assertEqual(len(habits), 2)

    def test_list_habits_by_periodicity(self):
        db = Database()
        db.clear_database()
        habit1 = Habit("Habit 1", "Description 1", "daily")
        habit2 = Habit("Habit 2", "Description 2", "weekly")
        db.add_habit(habit1)
        db.add_habit(habit2)
        daily_habits = [habit for habit in db.get_habits() if habit.periodicity == "daily"]
        weekly_habits = [habit for habit in db.get_habits() if habit.periodicity == "weekly"]
        self.assertEqual(len(daily_habits), 1)
        self.assertEqual(daily_habits[0].name, "Habit 1")
        self.assertEqual(len(weekly_habits), 1)
        self.assertEqual(weekly_habits[0].name, "Habit 2")

    def test_longest_run_streak_all_habits(self):
        db = Database()
        db.clear_database()
        habit1 = Habit("Habit 1", "Description 1", "daily")
        habit2 = Habit("Habit 2", "Description 2", "weekly")
        db.add_habit(habit1)
        db.add_habit(habit2)
        db.complete_task("Habit 1", datetime.now() - timedelta(days=1))
        db.complete_task("Habit 1", datetime.now())
        db.complete_task("Habit 2", datetime.now() - timedelta(weeks=1))
        db.complete_task("Habit 2", datetime.now())
        streaks = [habit.compute_streak() for habit in db.get_habits()]
        self.assertEqual(max(streaks), 2)

    def test_longest_run_streak_for_habit(self):
        db = Database()
        db.clear_database()
        habit = Habit("Test Habit", "This is a test habit", "daily")
        db.add_habit(habit)
        db.complete_task("Test Habit", datetime.now() - timedelta(days=1))
        db.complete_task("Test Habit", datetime.now())
        streak = next(habit.compute_streak() for habit in db.get_habits() if habit.name == "Test Habit")
        self.assertEqual(streak, 2)

if __name__ == "__main__":
    unittest.main()
