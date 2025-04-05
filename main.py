#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
School Timetable Generator
"""

### DO NOT MODIFY THE CODE BELOW THIS LINE ###

# Define the input constraints
classes = ["Class 6A", "Class 6B", "Class 7A", "Class 7B"]

subjects = ["Mathematics", "Science", "English", "Social Studies", "Computer Science", "Physical Education"]

class_subject_periods = {
    "Class 6A": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 3, "Physical Education": 3},
    "Class 6B": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 3, "Physical Education": 3},
    "Class 7A": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 4, "Physical Education": 2},
    "Class 7B": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 4, "Physical Education": 2}
}

teachers = {
    "Mr. Kumar": ["Mathematics"],
    "Mrs. Sharma": ["Mathematics"],
    "Ms. Gupta": ["Science"],
    "Mr. Singh": ["Science", "Social Studies"],
    "Mrs. Patel": ["English"],
    "Mr. Joshi": ["English", "Social Studies"],
    "Mr. Malhotra": ["Computer Science"],
    "Mr. Chauhan": ["Physical Education"]
}

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
periods_per_day = 6

### DO NOT MODIFY THE CODE ABOVE THIS LINE ###

import random
from collections import defaultdict

def assign_teacher(subject):
    available_teachers = [teacher for teacher, subs in teachers.items() if subject in subs]
    return random.choice(available_teachers)

def generate_timetable():
    timetable = {day: {period: {} for period in range(1, periods_per_day + 1)} for day in days_of_week}
    teacher_schedule = {teacher: {day: [None]*periods_per_day for day in days_of_week} for teacher in teachers}
    class_schedule = {cls: {day: [None]*periods_per_day for day in days_of_week} for cls in classes}
    
    for cls in classes:
        subject_periods = class_subject_periods[cls]
        subject_slots = []
        for subject, count in subject_periods.items():
            teacher = assign_teacher(subject)
            for _ in range(count):
                subject_slots.append((subject, teacher))
        random.shuffle(subject_slots)

        slot_index = 0
        for day in days_of_week:
            for period in range(periods_per_day):
                if slot_index >= len(subject_slots):
                    break
                subject, teacher = subject_slots[slot_index]

                # Check if teacher is available
                if teacher_schedule[teacher][day][period] is None:
                    teacher_schedule[teacher][day][period] = cls
                    class_schedule[cls][day][period] = (subject, teacher)
                    slot_index += 1
                else:
                    continue
    return class_schedule


def display_timetable(timetable):
    for cls in timetable:
        print(f"\nTimetable for {cls}:")
        print("-" * 60)
        print("{:<10} {:<10} {:<20}".format("Day", "Period", "Subject (Teacher)"))
        print("-" * 60)
        for day in days_of_week:
            for i in range(periods_per_day):
                entry = timetable[cls][day][i]
                if entry:
                    subject, teacher = entry
                    print(f"{day:<10} {i+1:<10} {subject} ({teacher})")
                else:
                    print(f"{day:<10} {i+1:<10} Free")
        print("-" * 60)


def validate_timetable(timetable):
    # Check if all classes meet required number of periods
    for cls, required_subjects in class_subject_periods.items():
        actual_count = defaultdict(int)
        for day in days_of_week:
            for period in timetable[cls][day]:
                if period:
                    subject, _ = period
                    actual_count[subject] += 1
        for subject, count in required_subjects.items():
            if actual_count[subject] != count:
                return False, f"{cls} does not have {count} periods of {subject} (has {actual_count[subject]})"
    return True, "Valid timetable."


def main():
    print("Generating school timetable...\n")
    timetable = generate_timetable()
    is_valid, message = validate_timetable(timetable)
    if is_valid:
        display_timetable(timetable)
    else:
        print(f"Failed to generate valid timetable: {message}")


if __name__ == "__main__":
    main()
