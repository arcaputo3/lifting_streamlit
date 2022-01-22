import json

import matplotlib.pyplot as plt
import pandas as pd

from typing import List, Dict

from utils import *

with open('processed_data/workouts.json', 'r') as file:
    workout_json_data = json.load(file)

all_exercises = pd.concat([pd.DataFrame(entry['exercises']) for entry in workout_json_data if 'exercises' in entry])

if __name__ == "__main__":
    x = 50
    volume = all_exercises['sets'].apply(exercise_volume_map).apply(sum).to_frame().set_index(all_exercises['name'])
    volume = volume.reset_index().groupby('name').sum()
    top_exercises = all_exercises.groupby('name')['sets'].count()
    print(volume)
    print(top_exercises)

    top_exercises.sort_values().iloc[-x:].plot(figsize=(10, 8), kind='barh')
    plt.xlabel('Frequency')
    plt.ylabel('Exercise')
    plt.title(f'Top {x} Exercises by Workout Frequency')
    plt.tight_layout()
    plt.savefig(f'processed_data/top_{x}_exercises_frequency.png')

    volume.sort_values(by='sets').iloc[-x:].plot(figsize=(10, 8), kind='barh')
    plt.xlabel('Volume (lbs)')
    plt.ylabel('Exercise')
    plt.title(f'Top {x} Exercises by Volume')
    plt.tight_layout()
    plt.savefig(f'processed_data/top_{x}_exercises_volume.png')
