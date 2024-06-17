# Mania

Because you'd have to be mad to build something this niche.

## About

### Idea and motivation

I had a bunch of Youtube playlists grouped by language or genre, that I wanted to be able
to manipulate freely. Easy detection of newly added and removed videos, generation of new playlists
that are an intersection of two playlists and possibly a self made music player.

Two out of three goals is not so bad. I never did make that music player.

### Dependencies and working

I have elected to use Python and the Youtube Data API v3 for retreival of information. Scripts
were considered but were tedious to write and had to be copied to files. I am happy with the
compromise I made there.

I could have continued using the API for playlist creation. That would have made the system
much more reliable, but the API requires OAUTH and guzzles through the alloted quota. Therefore
I elected to use a browser script that is slightly more tedious (as you have to copy paste and
manage data yourself as well as run it several times if needed) but simpler and more secure.

## Setup and usage

### For retreiving data

1. Git clone this repository.
2. pip install requirements.txt to get the API libraries.
3. Modify UserSettings.json to your liking and include API Key for Youtube Data Api v3
4. Modify run.py to retrieve and manage your playlist data.
5. (Optional) If needed, modification of logic.py to retreive and manage more information.

### For creating the new playlist

1. Set variable specific = Set(list of video ids) in script.js
2. Navigate to the playlist page you want to modify (see full playlist, scroll down to load it all)
3. Open developers console, clear it and wait about 30s. (To ensure loading complete)
4. Copy paste script.js into the console and let it run
5. You should see a queue being created with the relevant videos in it.
6. If not close and reopen the page and try again.

### About UserSettings.json

1. Set the API_KEY to be the value of your Youtube data api v3 key.
2. Set PATHS to be an object containing several sub MetricObjects
3. For each basic MetricObject has a path and backup for file storage.
4. Ensure that all filepaths end with /.
5. Every basic MetricObject has a categories object,
6. Every derived MetricObject has a categories list consisting of keys for two basic objects.

### IMPORTANT TO NOTE

1. The script.js is unstable and might break from DOM updates.
2. There seems to be a limit to how many videos can fit inside a YouTube Queue (150).
3. Script might need to be run multiple times before intended result. If so, refresh before.
4. The queue might have a few duplicate/missing videos. Extend logic.py functionality to verify result.