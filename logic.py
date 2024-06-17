from googleapiclient.discovery import build
from interface import API_KEY,PATHS

# Folder and path creation if it doesn't exist
from pathlib import Path
for obj in PATHS.values():
    my_file = Path(obj["path"])
    my_file.mkdir(parents=True, exist_ok=True)

    my_file = Path(obj["backup"])
    my_file.mkdir(parents=True, exist_ok=True)

class Item_Loader:
    """
        An object of this class is used to load the required playlistItems into a list. Playlist ID should be specified
        before calling self.loadItems(). Currently unsafe.
    """

    def __init__(self,youtube):
        self.youtube = youtube

    def loadItems(self,id):

        #Loading first batch of videos.
        request = self.youtube.playlistItems().list(part = "snippet",playlistId = id,maxResults = 50)
        response = request.execute()

        #Saving info.
        items = [item for item in response['items']]

        #Finding all other items and saving info.
        while("nextPageToken" in response):
            request = self.youtube.playlistItems().list(part = "snippet",playlistId = id,maxResults = 50,pageToken = response["nextPageToken"])
            response = request.execute()  
            
            items.extend(response['items'])

        return items
