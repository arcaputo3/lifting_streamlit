# This is a project for tracking, plotting, and optimizing workout progress
import os
import json
from typing import Any, Dict, List, Union

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

    def init_curr_exercise() -> Dict[str, Union[List, str]]:
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
                    'weight': int(entry[0][7:-3]),  # pounds by default
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
                    'distance': float(entry[0][7:-4]),  # miles by default
                    'time': entry[-1][1:]
                }
            else:
                curr_set = {
                    'time': entry[-4:]
                }
            curr_exercise['sets'].append(curr_set)
        elif entry.startswith('Notes: '):
            exercises[-1]['notes'] = entry[7:]
        elif entry.startswith('Workout Notes: '):
            output_data['workout_notes'] = entry.split(':')[1][1:]
        elif entry == '' and curr_exercise != init_curr_exercise():
            exercises.append(curr_exercise)
            curr_exercise = init_curr_exercise()
        elif strong_link not in entry:
            curr_exercise['name'] = entry
    if curr_exercise != init_curr_exercise():
        exercises.append(curr_exercise)
    output_data['exercises'] = exercises
    return output_data


def workouts_txt_to_json(txt_path: str, json_path: str):
    all_workout_data = [
        parse_workout_string(file_to_string(f'{txt_path}/{workout_file}'))
        for workout_file in sorted(os.listdir(txt_path), key=len)
        if workout_file.endswith('.txt')
    ]
    print(f"Processed {len(all_workout_data)} workouts! Saving to json...")
    with open(json_path, 'w', encoding='utf-8') as output_file:
        json.dump(all_workout_data, output_file, ensure_ascii=False, indent=4, sort_keys=True)
    print("Done!")


def exercise_volume_map(data: List[Dict[str, int]]) -> List[int]:
    return [
        max(d.get('weight', 0), 1) * d.get('reps', 0)
        for d in data
    ]


def epley_orm(data: List[Dict[str, int]]) -> List[float]:
    return [
        round(d.get('weight', 0) * (1 + d.get('reps', 0) / 30), 2)
        if d.get('reps', 0) != 1 else round(d.get('weight', 0), 2)
        for d in data
    ]


def lombardi_orm(data: List[Dict[str, int]]) -> List[float]:
    return [
        round(d.get('weight', 0) * d.get('reps', 0) ** 0.1, 2)
        for d in data
    ]


def mcglothin_orm(data: List[Dict[str, int]]) -> List[float]:
    return [
        round(d.get('weight', 0) * 100 / (101.3 - 2.67123 * d.get('reps', 0)), 2)
        if d.get('reps', 0) != 1 else round(d.get('weight', 0), 2)
        for d in data
    ]


def safe_max(data: List[float]):
    if not data:
        return 0
    return max(data)


if __name__ == '__main__':
    if 'processed_data' not in os.listdir():
        os.mkdir('processed_data')
    workouts_txt_to_json('workouts', 'processed_data/workouts.json')
