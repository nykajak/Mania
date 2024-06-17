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

class File_Manager:
    """
        An object of this class is used to generate and interact with files generated using data from Item_Loader class.
        It requires a filename attribute to target.
    """

    def __init__(self):
        pass

    def extractIds(self,filename = None):
        """
            Function is used to extract all the urls given filename. Returns None if filename not set.
        """

        if filename is None:
            return None

        with open(filename, "r") as f:
            ids = [line[:11:] for line in f.readlines()]

        return ids
    
    def extractInfo(self,filename = None):
        """
            Function is used to extract all the lines from filename. Returns None if filename not set.
        """

        if filename is None:
            return None
        
        with open(filename,"r") as f:
            content = f.readlines()
        
        return content

    def updateBasic(self,filename,res,verbose = True):
        """
            Function is used to populate filename using the returned result. Returns None if filename not set. 
            Not safe.
        """

        if filename is None:
            if verbose:
                print("No file is loaded!")

            return -1

        count = 0
        with open(filename,"w") as f:
            for item in res:
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_title = item["snippet"]["title"]
                f.write(f"{video_id},{video_title}\n")
                count += 1

        if verbose:
            print(f"{count} entries loaded into {filename}!")

        return 1
    
    def updateHybrid(self,src1,src2,destination,verbose = True):
        result = self.extractInfo(src1)
        if result is None:
            if verbose:
                print("src1 is None!")

            return -1
        s1 = set(result)
        
        result = self.extractInfo(src2)
        if result is None:
            if verbose:
                print("src2 is None!")
            return -1
        s2 = set(result)
    
        records = s1.intersection(s2)
        if verbose:
            print(f"{len(records)} entries found common in {src1} and {src2}!")

        with open(destination,"w") as f:
            f.writelines(records)

        if verbose:
            print(f"{len(records)} entries added to {destination}!")
            print()
        
        return 1