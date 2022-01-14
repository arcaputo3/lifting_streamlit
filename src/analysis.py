import json

import matplotlib.pyplot as plt
import pandas as pd

with open('processed_data/workouts.json', 'r') as file:
    workout_json_data = json.load(file)

all_exercises = pd.concat([pd.DataFrame(entry['exercises']) for entry in workout_json_data if 'exercises' in entry])

if __name__ == "__main__":
    x = 25
    top_exercises = all_exercises.groupby('name')['sets'].count()
    top_exercises.sort_values().iloc[-x:-1].plot(figsize=(10, 8), kind='barh')
    plt.xlabel('Frequency')
    plt.ylabel('Exercise')
    plt.title(f'Top {x} Exercises by Workout Frequency')
    plt.tight_layout()
    plt.savefig(f'top_{x}_exercises.png')
