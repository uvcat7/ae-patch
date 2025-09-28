import shutil, os
from pathlib import Path

if os.name == "nt":
    shutil.copy("GAME_PATCH.DAT", "C:\Program Files (x86)\Steam\steamapps\common\TGM4\GAME.DAT")
    shutil.copy("INFO_PATCH.DAT", "C:\Program Files (x86)\Steam\steamapps\common\TGM4\INFO.DAT")
    os.startfile("C:\Program Files (x86)\Steam\steamapps\common\TGM4\\tgm4.exe")
elif os.name == "posix":
    try:
        shutil.copy("GAME_PATCH.DAT", str(Path.home()) + "/.local/share/Steam/steamapps/common/TGM4/GAME.DAT")
        shutil.copy("INFO_PATCH.DAT", str(Path.home()) + "/.local/share/Steam/steamapps/common/TGM4/INFO.DAT")
    except FileNotFoundError:
        shutil.copy("GAME_PATCH.DAT", str(Path.home()) + "/Library/Application Support/Steam/steamapps/common/TGM4/GAME.DAT")
        shutil.copy("INFO_PATCH.DAT", str(Path.home()) + "/Library/Application Support/Steam/steamapps/common/TGM4/INFO.DAT")
