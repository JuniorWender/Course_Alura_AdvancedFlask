import os
from jogoteca import app

# ------------------------------------------------- Functions ----------------------------------------------------------------

def recovery_Image(id):
    for game_Cover in os.listdir(app.config['UPLOAD_PATH']): # create a list with all files on folder img
        if f'gameCover_{id}.jpg' == game_Cover:
            return game_Cover
        
    return 'default.jpg' # if the image not exists, return the default image