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
    
    def _saveFile(self, obj, label, verbose = True):
        src = f'{obj["path"]}{label}.txt'
        dest = f'{obj["backup"]}{label}.txt'

        with open(src,"r") as f:
            content = f.read()

        with open(dest,"w") as f:
            f.write(content)

        if verbose:
            print(f'Saved {label}.txt file')
    
    def saveFiles(self, verbose = True):
        for obj in PATHS.values():
            if type(obj["categories"]) != dict:
                cat_1 = PATHS[obj["categories"][0]]
                cat_2 = PATHS[obj["categories"][1]]

                for i in cat_1["categories"].keys():
                    for j in cat_2["categories"].keys():
                        label = f'{i}_{j}'
                        self._saveFile(obj,label,verbose)
            else:
                for label in obj["categories"].keys():
                    self._saveFile(obj,label,verbose)
    
    @staticmethod
    def _seeNew(f1,f2,verbose = True):
        with open(f1,"r") as f:
            s1 = set(f.readlines())

        with open(f2,"r") as f:
            s2 = set(f.readlines())
        
        if len(s1) > len(s2):
            if verbose:
                print(f"{f1} has {len(s1) - len(s2)} new records!")
            
            return s1.difference(s2)
        
        if verbose:
            print(f"{f1} has no new records.")

        return False
    
    @staticmethod
    def seeAllNew(verbose = True):
        d = {}
        for obj in PATHS.values():
            if type(obj["categories"]) != dict:
                cat_1 = PATHS[obj["categories"][0]]
                cat_2 = PATHS[obj["categories"][1]]

                for i in cat_1["categories"].keys():
                    for j in cat_2["categories"].keys():
                        label = f'{i}_{j}.txt'
                        main_file = f'{obj["path"]}{label}'
                        backup_file = f'{obj["backup"]}{label}'
                        d[main_file] = File_Manager._seeNew(main_file,backup_file,verbose)
            
            else:
                for label in obj["categories"].keys():
                    main_file = f'{obj["path"]}{label}.txt'
                    backup_file = f'{obj["backup"]}{label}.txt'
                    d[main_file] = File_Manager._seeNew(main_file,backup_file,verbose)
        
        return d
    
    @staticmethod
    def _checkValid(f1,f2,verbose = True):
        with open(f1,"r") as f:
            s1 = set(f.readlines())

        with open(f2,"r") as f:
            s2 = set(f.readlines())

        if s1.issuperset(s2):
            if verbose:
                print(f"Compared {f1} and {f2}. All OK.")
            return True

        res = s2.difference(s1)
        if verbose:
            print(f"Compared {f1} and {f2}. {len(res)} discrepencies found!")

        return res
    
    @staticmethod
    def checkAllValid(verbose = True):
        d = {}
        for obj in PATHS.values():
            if type(obj["categories"]) != dict:
                cat_1 = PATHS[obj["categories"][0]]
                cat_2 = PATHS[obj["categories"][1]]

                for i in cat_1["categories"].keys():
                    for j in cat_2["categories"].keys():
                        label = f'{i}_{j}'
                        main_file = f'{obj["path"]}{label}.txt'
                        backup_file = f'{obj["backup"]}{label}'
                        d[main_file] = File_Manager._checkValid(main_file,backup_file,verbose)
            
            else:
                for label in obj["categories"].keys():
                    main_file = f'{obj["path"]}{label}.txt'
                    backup_file = f'{obj["backup"]}{label}.txt'
                    d[main_file] = File_Manager._checkValid(main_file,backup_file,verbose)
        
        return d
    
class Updater:
    def __init__(self):
        youtube = build("youtube","v3",developerKey=API_KEY)

        self.item_loader = Item_Loader(youtube)
        self.file_manager = File_Manager()

    def updateAllBasic(self, verbose = True):
        for obj in PATHS.values():
            if type(obj["categories"]) != dict:
                continue
            
            for label,id in obj["categories"].items():
                filename = f'{obj["path"]}{label}.txt'
                res = self.item_loader.loadItems(id)
                self.file_manager.updateBasic(filename,res,verbose)

    def updateAllHybrid(self, verbose = True):
        for obj in PATHS.values():
            if type(obj["categories"]) != list:
                continue
            
            cat_1 = PATHS[obj["categories"][0]]
            cat_2 = PATHS[obj["categories"][1]]

            for i in cat_1["categories"].keys():
                for j in cat_2["categories"].keys():
                    src1 = f'{cat_1["path"]}{i}.txt'
                    src2 = f'{cat_2["path"]}{j}.txt'
                    dest = f'{obj["path"]}{i}_{j}.txt'
                    self.file_manager.updateHybrid(src1,src2,dest,verbose)

    def updateAll(self,verbose = True):
        self.updateAllBasic(verbose)
        self.updateAllHybrid(verbose)
            