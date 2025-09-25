import shutil,os

shutil.copy("GAME_PATCH.DAT", "C:\Program Files (x86)\Steam\steamapps\common\TGM4\GAME.DAT")
shutil.copy("INFO_PATCH.DAT", "C:\Program Files (x86)\Steam\steamapps\common\TGM4\INFO.DAT")
os.startfile("C:\Program Files (x86)\Steam\steamapps\common\TGM4\\tgm4.exe")