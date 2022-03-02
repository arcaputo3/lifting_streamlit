# lifting_streamlit
Project for analyzing workout data imported from Strong 

## Setup
*Shift-click links to avoid navigating away from links.*
1. Download and install [git](https://git-scm.com/)
2. Clone this repo to your local machine by running `git clone https://github.com/arcaputo3/lifting_streamlit.git` or, create a fork and clone that (recommended)
3. Download the [Strong App](https://www.strong.app/) to your smart phone and record your workouts there
4. Download and install the latest version of [Docker](https://www.docker.com/) (4.5.1 as of writing this)
5. Export workouts in `.txt` format to `~/lifting_streamlit/workouts`. Here is a [guide](https://help.strongapp.io/article/109-share-workout-or-routine) - for best results, clone this repo to a cloud location accessible by your phone (using iCloud for instance)
6. Navigate to the `~/lifting_streamlit` folder locally via terminal 
7. Run `docker compose build`
8. Run `docker compose up`
9. Navigate to http://localhost:8501/ in your browser to view the dashboard!

### Exporting workouts without Strong App
Workout files can be created manually! Example format:
```angular2html
Push 1
Monday, July 19, 2021 at 10:45 AM

Bench Press (Barbell)
Set 1: 135 lb × 3
Set 2: 185 lb × 3
Set 3: 225 lb × 2
Set 4: 255 lb × 2
Set 5: 265 lb × 2
Set 6: 265 lb × 2
Set 7: 225 lb × 3
Set 8: 225 lb × 3
Set 9: 225 lb × 3

Chest Dip
Set 1: 5 reps
Set 2: +35 lb × 8
Set 3: +35 lb × 8
Set 4: +35 lb × 8

Incline Bench Press (Dumbbell)
Set 1: 65 lb × 12
Set 2: 65 lb × 12
Set 3: 65 lb × 9

Incline Chest Fly (Dumbbell)
Set 1: 25 lb × 12
Set 2: 25 lb × 12
Set 3: 25 lb × 10

Watt Bike
Set 1: 8 mi | 0:30
```
Note the use of `×` vs. `x`!

### Feature Requests
You can open issues in this repo, but I ask that you please fork and create your own pull request if you would like features added. I will be adding features as I see fit, but likely very slowly...
