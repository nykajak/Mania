from logic import Updater

if __name__ == "__main__":
    updater = Updater()
    
    # To create file structure and retrieve data. Calls API
    # updater.updateAll()
    
    # To save by overwriting backups
    # updater.file_manager.saveFiles()

    # To check if new records added
    # updater.file_manager.seeAllNew()

    # To check if old records maintained
    # updater.file_manager.checkAllValid()

    # To get urls of hybrid file
    # filename = "./MySongs/Hybrid/malayalam_feels.txt"
    # updater.file_manager.extractIds(filename)