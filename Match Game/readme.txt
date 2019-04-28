/*
This is the readme file for a tkinter based card matching game
written in python3
FILE: readme.txt
CREATED ON: 2019/04/29
CREATED BY: Isaac Powrie
*/

THE PROJECT
This project was about creating a simple game using tkinter and
python3. The game is a card matching game, with 16 cards being
generated 2x each. There are two classes which the application
uses:
	GAME:
The game class contains the logic for the game play. the game loads
the .png images from the images folder and formats them for use by
tkinter as images on button widgets. This class also contains the 
functional logic for flipping the cards, tracking how many cards
are face up, checking to see if the two chosen cards which are face
up match, and to store the cards which are successfully matched. The
game shuffles the cards into a random pattern at the beginning of 
each game.
	GALLERY:
The gallery class takes a list of images and displays them to the
user. The only functionality of the gallery is clicking through the 
images from beginning to end and back to the beginning, etc. In the
context of the matching game, the gallery is a storage of the 
successful matches from the current game, and the gallery gives
players a chance to scroll through the images they have successfully 
captured

LIMITATIONS
The game is very simple, it requires a folder named images with one
file named back.png for the card backs and a subfolder labeled gallery
which contains the 16 .png images for matching. These images will be
formatted to an aspect ratio of 3 Height : 2 Width in both the game and
the gallery. As long as these specifications are followed, there is no
need to use the images I created. The game also requires python3 with the 
tkinter and PIL libraries installed.

** an anomally occurs in gameplay if you double click your selections
because the game detects the second click as an independant event and 
proccesses it after intended functionality has taken place. This can 
result in cards appearing to stay face up when they should turn themselves 
down, but actually the computer is turning them down and then very quickly
registering a second selection of the same card.

