#Python Jeopardy

Branched off of my previous Jeopardy Scoreboard, this is my own rendition of a Jeopardy-style game intended for larger audiences. Create a "board" using the Editor.py script, then open it with Jeopardy.py and start playing!

[Here are a few images of the game. (OLD; need to make new ones eventually)](http://imgur.com/a/nkiKA)

##Editor

The editor allows you to easily create a board to use with the game. Change rounds through the menu. Edit the category name by typing in the box (this may be updated to it's own popup window due to the lack of wrap in Tkinter's Entry). Click on a box to edit that question. The points assigned to each question can be changed through the "Change Point Values" menu button. Images can be added to the "question" Frame by clicking the "Add Image" button, then typing the full path to the image (I acknowledge this is tedious, however file-browsing open dialogs are well beyond my abilities) (also, the image system has plans to be more customizable by giving the choice between the question/answer Frames, and above or below the text).

The files will be saved in a folder named ".PythonJeopardy" found wherever Python's working directory may be (in Linux, this would be `~/.PythonJeopardy`, I have no idea where it will be found on other OSes). The "Open" button will populate with the possible files (*.board) found in the `~/.PythonJeopardy` folder. The ".board" files are massive, one-line-a-piece arrays that would be nearly impossible to follow by reading, so if you need a readable file (such as for making a cheat-sheet or showing the content to another person), use the "Save human-readable .txt" menu, then I suggest using a document editor to better optimize your page usage.

##Game

The game is currently set up to allow for either two teams or three individuals to compete (realistically, it could be 3 teams too, but that's definitely more work than I want to do). The "Open" button will populate with the possible files (*.board) found in the `~/.PythonJeopardy` folder. Putting the board on a larger screen/projector is suggested. When you have the window sized properly for your game, press the "Auto Font Size" button to scale the font size to the window (this will change how a few display elements are determined). The clock can be handled manually through the scoreboard on the bottom or set to automatically start when a question loads. The scoring can be switched between a 2-button system, where each person/team gets the question's full value added or subtracted from their score, or a more manual scoring system, where buttons for the highest point value, the lowest point value, and half of the lowest point value are made. This second system allows for easier implementation of custom scoring, which you can find examples of in the Example Rules document.

##Possible future work

*  Game
  *  Test the effectiveness of the "Auto Font Size" on bigger monitors.
*  Editor
  *  Add keybinds for switching categories. (Implementation difficulty: low-mid; Priority: very low)
  *  Revisit code and try to make it not so slow (Implementation difficulty: high; Priority: mid)
*  Both
  *  Change how images are handled to a more customizable format. (Implementation difficulty: mid-high; Priority: mid-high)
