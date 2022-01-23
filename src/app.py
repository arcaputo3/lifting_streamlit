import json
from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from utils import exercise_volume_map, epley_orm, mcglothin_orm, lombardi_orm, safe_max

plt.style.use('ggplot')
# pd.options.plotting.backend = "plotly"

global_unit_selectbox = st.sidebar.selectbox(
    'Weight Units',
    ('LB', 'KG')
)

def plot_exercise_volume(data: pd.DataFrame, exercise_name: Union[str, List[str]], units: str = global_unit_selectbox):
    if isinstance(exercise_name, str):
        new_data = data[data['name'] == exercise_name]
    else:
        new_data = data[data['name'].isin(exercise_name)]
    new_data = new_data['sets'].apply(exercise_volume_map).apply(sum).to_frame().rename(columns={'sets': 'Volume'})
    new_data['Average Volume'] = new_data['Volume'].expanding().mean()
    new_data['Max Volume'] = new_data['Volume'].cummax()
    if units == 'KG':
        new_data /= 2.2
    new_data.plot(figsize=(10, 8))
    plt.title(f"Training Volume per {exercise_name} Training Session")
    plt.xlabel("Training Date")
    plt.ylabel(f"Weight ({units})")
    st.pyplot(fig=plt)


def plot_exercise_max(data: pd.DataFrame, exercise_name: Union[str, List[str]], max_column: str = 'epley_orm_max', units: str = global_unit_selectbox):
    if isinstance(exercise_name, str):
        new_data = data[data['name'] == exercise_name][max_column]
    else:
        new_data = data[data['name'].isin(exercise_name)][max_column]
    if units == 'KG':
        new_data /= 2.2
    new_data.plot(figsize=(10, 8), label='Max Training 1RM')
    new_data.expanding().mean().plot(label='Expanding Mean Training 1RM')
    new_data.cummax().plot(label='All Time Projected 1RM')
    plt.title(f"Training Max per {exercise_name} Training Session")
    plt.xlabel("Training Date")
    plt.ylabel(f"Weight ({units})")
    plt.legend()
    st.pyplot(fig=plt)


def plot_top_n(data: pd.DataFrame, asof: str, top_n: int = 25, units: str = global_unit_selectbox):
    data = data.loc[:asof]
    adjustment = (1 if units == 'LB' else 2.2)
    volume_base = data['sets'].apply(exercise_volume_map).apply(sum).to_frame().rename(columns={'sets': 'volume'})
    volume_base['name'] = data['name']
    volume_base['date'] = data.index
    volume = volume_base.groupby('name').sum() / adjustment
    cumulative_volume = volume_base.groupby('date').sum() / adjustment
    top_exercises = data.groupby('name')['sets'].count()
    top_n_frequency = top_exercises.sort_values().iloc[-top_n:]
    top_n_volume = volume.sort_values(by='volume').iloc[-top_n:]

    top_n_frequency.plot(figsize=(10, 8), kind='barh')
    plt.xlabel('Frequency')
    plt.ylabel('Exercise')
    plt.title(f'Top {top_n} Exercises by Workout Frequency')
    st.pyplot(fig=plt)

    top_n_volume.plot(figsize=(10, 8), kind='barh')
    plt.xlabel(f'Volume ({units})')
    plt.ylabel('Exercise')
    plt.title(f'Top {top_n} Exercises by Volume')
    st.pyplot(fig=plt)

    cumulative_volume.cumsum().plot(figsize=(10, 8))
    plt.title(f'Total Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel(f'Volume ({units})')
    st.pyplot(fig=plt)

    cumulative_volume.expanding().mean().plot(figsize=(10, 8))
    plt.title(f'Average Volume Per Workout Over Time')
    plt.xlabel('Date')
    plt.ylabel(f'Volume ({units})')
    st.pyplot(fig=plt)


with open('processed_data/workouts.json', 'r', encoding="utf8") as file:
    workout_json_data = json.load(file)

all_exercises = pd.concat([
    pd.DataFrame(
        entry['exercises'],
        index=[entry['date'] for _ in entry['exercises']]
    )
    for entry in workout_json_data
    if 'exercises' in entry
])
all_exercises.index = pd.to_datetime(all_exercises.index)
all_exercises = all_exercises.sort_index()
all_exercises['volume'] = all_exercises['sets'].apply(exercise_volume_map)
all_exercises['epley_orm'] = all_exercises['sets'].apply(epley_orm)
all_exercises['mcglothin_orm'] = all_exercises['sets'].apply(mcglothin_orm)
all_exercises['lombardi_orm'] = all_exercises['sets'].apply(lombardi_orm)
for column in ['volume', 'epley_orm', 'mcglothin_orm', 'lombardi_orm']:
    all_exercises[column + '_max'] = all_exercises[column].apply(safe_max)

add_selectbox = st.sidebar.selectbox(
    'Analysis Type',
    ('Total', 'By Exercise', 'SBD Only')
)
sbd_columns = [
    'Bench Press (Barbell)'
    'Deadlift (Barbell)',
    'Squat (Barbell)'
]

if add_selectbox == 'Total':
    st.title("Aggregate Exercise Analysis")
    top_n_selected = st.slider(
        "How Many Exercises?",
        min_value=5,
        max_value=50,
        value=25
    )
    start_time = st.slider(
        "As of When?",
        min_value=all_exercises.index[0].to_pydatetime(),
        max_value=(end_time := all_exercises.index[-1].to_pydatetime()),
        format="YYYY-MM-DD",
        value=end_time
    )
    plot_top_n(all_exercises, start_time, top_n_selected)

elif add_selectbox == 'By Exercise':
    st.title("Individual Exercise Analysis")
    exercise_selected = st.selectbox("Training Max Analysis", sorted(list(all_exercises['name'].unique())), index=5)
    max_type_lookup = {
        'Epley': 'epley_orm_max',
        'McGlothin': 'mcglothin_orm_max',
        'Lombardi': 'lombardi_orm_max'
    }
    max_type = st.radio("1RM Calculation", sorted(max_type_lookup.keys()))
    plot_exercise_max(all_exercises, exercise_selected, max_type_lookup[max_type])
    plot_exercise_volume(all_exercises, exercise_selected)

elif add_selectbox == 'SBD Only':
    plot_exercise_volume(all_exercises, sbd_columns)

