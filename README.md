# ae-patch
Basic graphics modding framework for Tetris The Grandmaster 4: Absolute Eye.

The framework is still work-in-progress, but any graphic can be changed, as long as the resolution and format of the changed graphics are the same.

# Requirements
Python 3 is required. The `pylzss` package is needed:

`python3 -m pip install pylzss`

Optionally, the `Wand` library and [ImageMagick](https://imagemagick.org/script/download.php#windows) binaries are needed if you want the .dds files to be converted to .png when extracting game files:
`python3 -m pip install Wand`

TGM4 is a Windows-only game, so these scripts assume you are using Windows.

[Paint.NET](https://www.getpaint.net/) is recommended for editing the .dds files that the game uses. Installing it also shows an image preview for .dds files in Windows Explorer.

# File explanation
TGM4's files are LZSS-compressed, with the exception of the audio files. The files are stored in GAME.DAT and their index information is stored in INFO.DAT. The INFO.DAT data is obfuscated with a simple rot, XOR, and 16-byte key specified in the file.

The graphics data is stored in three main file types:
* .twx: this corresponds to DirectX Texture (.dds) files. The only difference between a .dds file and a .twx file is the header, and the texture information itself is identical.
* .eff: these are the animation files, hence the extension's name ("effects"). These contain a set of graphics files used to build an animation, as well as a list of animation types and rendering information.
* .mdl: these are a list of modeling files, with a set of vertex information (.vwx) that ties a set of textures (.twx/.txs) files together.

The .txs ("TeXtureSet"?) file type contains a list of textures but doesn't include the .twx files in the format unless the set is inside a .mdl or .eff file.


# Instructions

## 01_Extract_Dat.py
Running this Python script will grab GAME.DAT and INFO.DAT from the game's Steam install folder and extract all the files contained therein to /data.

## 02_Graphics_Convert.py
This script extracts all the graphics data from the files in /data.

The .twx files will be extracted to /images in .dds format, keeping their appropriate path.

The .twx files in .eff and .mdl files will be extracted to /dataeff, with their .eff/.mdl file included as part of the path. Then they will be extracted to /imageseff in .dds format.

## 03_Patch_Textures.py
Now, modify whatever .dds files in the /images or /imageseff folder you'd like.

Once you want to patch the game, run this script. It will build all the .twx, .eff, and .mdl files from the .dds files and copy them to the /datapatch folder, keeping the existing file structre.
This folder can be used to patch *any* file in the game, not just graphics files.

## 04_Rebuild_Dat.py
This file will rebuild GAME_PATCH.DAT and INFO_PATCH.DAT, using only the /data and /datapatch folders.
/data is used as the master reference for which files to include. If you want to add a new file to the game for some reason, you'll need to add it here.
/datapatch is used as a patching reference. If a file in /datapatch is different than the file in /data, it will be included in the GAME_PATCH.DAT file.

## 05_Patch_Game.py
This script will copy GAME_PATCH.DAT and INFO_PATCH.DAT back to your Steam folder and start TGM4.
The unmodified GAME.DAT and INFO.DAT will still be in this folder in case there is an issue.

