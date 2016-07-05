# Name That Tune!
A simple Python program to manage playing a "Name That Tune"-style game with up to 10 teams/players! Probably best used for larger groups of people, such as a party or convention.

This is version 2.0, and is a complete rewrite of what I had posted originally under my "Random Projects" repo. Assuming VLC still ships with cvlc under Windows/OSX, and assuming the syntax is the same, this should be 100% cross platform.

## Requirements
vlc (cvlc), and Tkinter, built on Python 2.7.11

##How To
Running the script for the first time should create ~/.NTT and ~/.NTT/SongList.txt. Use whatever audio editing software to create the clips you want to play, then export them in ascending numerical order as .mp3s in the ~/.NTT folder starting with "1.mp3". As you do this, run this script and press "Launch Editor" to add the relevent song information to the SongList.txt file (artist, song name, tv show, whatever). If all is done correctly, pressing "Launch Board" will randomize the songs, start a countdown of how many songs remain, then turn the first window into a control panel and launch a new window for use on a projector or second monitor (I recommend maximizing both the control window and the game window, then pressing the "Auto-adjust font" button to update the font to fill a readable amount of the screen). To prevent premature exposure of the song information, the "reveal" buttons only become active after the clip is played. Once time runs out or once all song information is exposed, pressing the "Reset" button will reset the clock, hide the information on the game screen, pull up the next random song, and deactivate the "reveal" buttons.

##Possible future work
- Be able to change the number of information fields for each song (currently set up for only song and show information for naming intro/outro themes for different shows)
- Add directory support for different sets of audio for different games
