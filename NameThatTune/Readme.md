# Name That Tune!
A simple Python program to manage playing a "Name That Tune"-style game with up to 10 teams or players! Probably best suited for events with larger groups of people, such as a party or convention.

This is version 3.0, and is a complete rewrite of what I had posted originally under my "Random Projects" repo. This should be 100% cross platform, although is not verified to work on anything other than Linux.

[Here are some (old) images of the game](http://imgur.com/a/8062S)

## Requirements
* Python3 (built using 3.6)
* simpleaudio
* tkinter

## How To

### Building your game
First, run the script. It will create `~/.NTT` and `~/.NTT/SongList.txt`, and will open a blank window. Use the audio editing software of your choice to create the clips you want to play, then export them in `.wav` format in the `~/.NTT` folder. In the game window, press "Launch Editor" to bring up a simple window to add the relevent song information to `~/.NTT/SongList.txt` (two fields of information plus the filename of the clip are supported). Everything is saved as you go. If you need to remove a song, open `~/.NTT/SongList.txt` in your text editor of choice and delete the entire line you want gone and save. It is not recommended to edit this file directly due to syntax issues. To edit a song's information, delete the line and re-enter it using the game's editor. *(Note: If you change `~/.NTT/SongList.txt` manually, you will need to restart the script for these changes to apply)*

### Running your game
Once all the desired clips have been added, close out of the editor and press "Launch Board". The songs will be randomized and a new window will open with a countdown timer, a blacked-out area, and team scores (the "game board"). This window should be displayed on another monitor or a projector. The main window will set up in a similar fashion and turn into your "control board". This window should be displayed on a monitor only you can see. Resize the windows to your desired size and press the "Auto-adjust font size" button to get the best-fit font size for your displays.

Most buttons on the control board are self-explanatory. The "Play song" button will turn into the "Reset" button when the button is pressed; the "Reset" button will stop the song playback, hide any lines revealed on the game board, and skip to the next song in the list. Songs can be skipped, returned to, or played without starting the clock using the "Navigation" menu.

## Possible (but not probable) future work
- Be able to change the number of information fields for each song (currently set up for only song and show information for naming intro/outro themes for different shows)
- Add directory support for different sets of audio for different games
