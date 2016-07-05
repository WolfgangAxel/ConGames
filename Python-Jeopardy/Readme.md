#Python Jeopardy

Branched off of my previous Jeopardy Scoreboard, this is my own rendition of a Jeopardy-style game intended for larger audiences. Create a "board" using the Editor.py script, then open it with Jeopardy.py and start playing!

[Here are a few images of the game.](http://imgur.com/a/nkiKA)

##Editor

The editor allows you to easily create a board to use with the game. Each category has it's own Frame which is loaded and unloaded as the next/previous buttons are pressed. The "Question" text box is where you would type the "Clue" that is initially shown to the people playing (the nomenclature used in this scripe will eventually be updated to at least somewhat mirror the game show). The points assigned to each question can be changed through the "Change Point Values" menu button. Images can be added to the "question" Frame by clicking the "Add Image" button, then typing the full path to the image (I acknowledge this is tedious, however file-browsing open dialogs are well beyond my abilities) (also, the image system has plans to be more customizable by giving the choice between the question/answer Frames, and above or below the text).

The files will be saved in a folder named ".PythonJeopardy" found wherever Python's working directory may be (in Linux, this would be `~/.PythonJeopardy`, I have no idea where it will be found on other OSes). The "Open" button will populate with the possible files found in the `~/.PythonJeopardy` folder. The ".board" files are massive, one-line arrays that would be nearly impossible to follow by reading, so if you need a readable file (such as for making a cheat-sheet or showing the content to another person), use the "Save human-readable .txt" button (the saving system will be replaced with one more like the opening system).

##Game

The game is currently set up for two teams to compete (there may be an update to allow for a custom number of teams/players in the future). The "Open" button will populate with the possible files found in the `~/.PythonJeopardy` folder. Putting the board on a larger screen/projector is suggested. When you have the window sized properly for your game, press the "Auto Font Size" button to scale the font size to the window (this will change how a few display elements are determined). Currently, the clock and the scoring are handled manually through the scoreboard on the bottom. This is to allow for easy accommodation of the user's personal set of rules. For example, I implement a stealing mechanic which awards half points for a correct answer, and I prefer to start the clock after I have finished reading the question. An "automatic" mode may be implemented, where the clock starts immediately and only full points are awarded or deducted.

##Future work

*  Game
  *  Change between Automatic and Manual scoring/clock.  (Implementation difficulty: low; Priority: low)
  *  Add system to change the number of scores/teams playing (Implementation difficulty: high; Priority: very low)
  *  Change point buttons to update to the highest, lowest, and half of the lowest values when a new board is loaded. (Implementation difficulty: mid-high; Priority: low)
  *  Add the scoreboard frame to the "Auto Font Size" function. (Implementation: mid-high; Priority: mid-high)
  *  Test the effectiveness of the "Auto Font Size" on bigger monitors.
  *  Remove font dependencies (Implementation difficulty: very low; Priority: high)
*  Editor
  *  Add keybinds for switching categories. (Implementation difficulty: low-mid; Priority: low)
  *  Change how the saving system works to use a menu. (Implementation difficulty: low; Priority: mid-high)
*  Both
  *  Change "Question" to "Clue" to avoid any confusion with real Jeopardy nomenclature (Implementation difficulty: low; Priority: mid)
  *  Add support for a "Final Jeopardy" round. (Implementation difficulty: mid-high; Priority: mid-low)
  *  Change how images are handled to a more customizable format. (Implementation difficulty: mid-high; Priority: mid-high)
