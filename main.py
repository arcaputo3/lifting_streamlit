# This is a project for tracking, plotting, and optimizing workout progress
import os
import json
from typing import Any, Dict

# TODO: Add docstrings
# TODO: Enable routing instead of if-elif`s
# TODO: Investigate regex


def file_to_string(filename: str) -> str:
    with open(filename, 'r', encoding="utf-8") as file:
        data = file.read()
        return data


def parse_workout_string(workout_string: str) -> Dict[str, Any]:
    workout_data = workout_string.split('\n')
    output_data = {
        'template': workout_data[0],
        'date': workout_data[1],
    }
    exercise_log = [
        x for x in workout_data[2:]
    ]
    exercises = []

    def init_curr_exercise() -> dict:
        return {'sets': []}

    curr_exercise = init_curr_exercise()

    cardio = '|'
    ds_str = '[Drop Set]'
    rpe = '@'
    reps = 'reps'
    strong_link = 'https://strong.app.link'
    times = '×'
    wu_str = '[Warm-up]'

    # Parse exercise log into correct output
    for idx, entry in enumerate(exercise_log):
        if entry.startswith('Set '):
            if times in entry:
                entry = entry.split(times)
                curr_set = {
                    'weight': int(entry[0][7:-3]),
                }
                if wu_str in entry[-1]:
                    curr_set['reps'] = int(entry[-1][-2 - len(wu_str):-len(wu_str)])
                    curr_set['warm_up'] = True
                if ds_str in entry[-1]:
                    curr_set['reps'] = int(entry[-1][-2 - len(ds_str):-len(ds_str)])
                    curr_set['drop_set'] = True
                if rpe in entry[-1]:
                    split_entry = entry[-1].split(f' {rpe} ')
                    curr_set['reps'] = int(split_entry[0])
                    curr_set['rpe'] = float(split_entry[-1])
                if 'reps' not in curr_set:
                    curr_set['reps'] = int(entry[-1][1:])
            elif reps in entry:
                curr_set = {'reps': int(entry.split(': ')[-1][:2].strip())}
                if wu_str in curr_set:
                    curr_set['warm_up'] = True
            elif cardio in entry:
                entry = entry.split(cardio)
                curr_set = {
                    'distance': entry[0][7:-3],
                    'time': entry[-1][1:]
                }
            else:
                curr_set = {
                    'time': entry[-4:]
                }
            curr_exercise['sets'].append(curr_set)
        elif entry.startswith('Notes: '):
            exercises[-1]['notes'] = entry[7:]
        elif entry == '' and curr_exercise != init_curr_exercise():
            exercises.append(curr_exercise)
            curr_exercise = init_curr_exercise()
        elif strong_link not in entry:
            curr_exercise['name'] = entry
    if curr_exercise != init_curr_exercise():
        exercises.append(curr_exercise)
    output_data['exercises'] = exercises
    return output_data


def workouts_txt_to_json(txt_path: str = 'workouts', json_path: str = 'processed_data/workouts.json'):
    all_workout_data = []
    for workout_file in os.listdir(txt_path):
        all_workout_data.append(parse_workout_string(file_to_string(f'{txt_path}/{workout_file}')))
    print(f"Processed {len(all_workout_data)} workouts! Saving to json...")
    with open(json_path, 'w', encoding='utf-8') as output_file:
        json.dump(all_workout_data, output_file, ensure_ascii=False, indent=4)
    print("Done!")


if __name__ == '__main__':
    workouts_txt_to_json()
