#! /usr/bin/python3

import random, time, os
import tkinter as tk
from PIL import Image, ImageTk

class Gallery ():
	"""Creates a simple click through gallery"""
	def __init__(self, root, images):
		self.root = root
		self.idx = 0
		self.frame = tk.Frame(root, width=816, height=608, bg="white")
		self.frame.pack_propagate(0)
		self.images = images
		self.pyImages = []
		self.current_image = ""
		self.frame.pack( side=tk.LEFT )
		self.load_images()
		self.load_button()
		
	def load_images(self):
		"""Turns images  into tkinter pyimages"""
		for i in range(0, len(self.images)):
			imagePil = Image.open(self.images[i])
			self.pyImages.append(ImageTk.PhotoImage(imagePil))
			
	def load_button(self):
		"""Loads the visualization of the gallery as a button"""
		self.current_image = tk.Button(self.frame, image=self.pyImages[0])
		self.current_image.config(command=self.scroll)
		self.current_image.pack(side=tk.LEFT, padx=208, pady=4)
		
	def refresh_gallery(self, images):
		"""Refreshes the gallery of images"""
		newPyImages = []
		for image in images:
			imagePil = Image.open(image).resize((400, 600))
			newPyImages.append(ImageTk.PhotoImage(imagePil))
		self.pyImages = newPyImages
		self.idx = 0
		self.current_image.config(image=self.pyImages[self.idx])	
			
	def scroll(self):
		"""
		Scrolls one object through the images in the pyImages gallery
		"""
		if self.idx < len(self.pyImages) - 1:
			self.idx += 1
		else:
			self.idx = 0
		self.current_image.config(image=self.pyImages[self.idx])


class Game():
	"""Creates a gameboard for a matching type game"""
	def __init__ (self, root, images, background):
		# setup main data members for content
		self.root = root
		self.frame = tk.Frame(root, width=816, height=608, bg="white")
		self.frame.pack_propagate(0)
		self.images = images
		backgroundPil = Image.open(background).resize((100, 150))
		self.background = ImageTk.PhotoImage(backgroundPil)
		self.cards = []
		self.pyImages = []
		self.buttons = []
		# setup data members for game play
		self.numCardsUp = 0
		self.matchImages = []
		# load start of game
		self.frame.pack( side=tk.LEFT )
		self.load_images()
		self.load_cards()
		self.display_cards()
		
	def load_images(self):
		"""
		Resize image into card size, and then load it into the 
		pyImages list
		"""
		for i in range(0, len(self.images)):
			imagePil = Image.open(self.images[i]).resize((100, 150))
			self.pyImages.append(ImageTk.PhotoImage(imagePil))
		
	def load_cards(self):
		"""
		Load the images, backgrounds, and randomized order into the
		cards list
		"""
		for i in range(0, 2):
			for i in range(0, len(self.pyImages)):
				newCard = [self.background, self.pyImages[i], 0, i]
				self.cards.append(newCard)
		random.shuffle(self.cards)	
		
	def display_cards(self):
		"""
		Create the cards as buttons and dsiplay them in the frame
		"""
		rowVal = 0
		colVal = 0
		for i in range(0, len(self.cards)):
			newButton = tk.Button(self.frame, image=self.cards[i][0], text=i)
			self.buttons.append(newButton)
			newButton.config(command=lambda idx = i: self.flip_card(idx))
			newButton.grid(column=colVal, row=rowVal, padx=1, pady=1)
			if colVal < 7:
				colVal += 1
			else:
				colVal = 0
				rowVal += 1
		
	def clear_cards(self):
		"""clear the cards to prepare for reloading"""
		self.cards = []
		
	def flip_card(self, idx):
		"""flip card if card is not already flipped"""
		if self.cards[idx][2] == 0:
			self.numCardsUp += 1
			self.buttons[idx].config(image=self.cards[idx][1])
			self.cards[idx][2] = 1
			if self.numCardsUp == 2:
				self.buttons[idx].update()
				self.root.after(1000)
				self.determine_match()
				self.numCardsUp = 0			
			
	def determine_match(self):
		"""determine if flipped cards have matched images"""
		# find the two flipped up cards
		selected = []
		for idx in range(0,len(self.cards)):
			if self.cards[idx][2] == 1:
				selected.append(self.cards[idx])
		# compare images on cards
		if selected[0][1] == selected[1][1]:
			self.matchImages.append(self.images[selected[0][3]])
			for idx in range(0, len(self.cards)):
				if self.cards[idx][2] == 1:
					self.cards[idx][2] = 2
		else:
			for idx in range(0,len(self.cards)):
				if self.cards[idx][2] == 1:
					self.cards[idx][2] = 0
					self.buttons[idx].config(image=self.cards[idx][0])
					

def load_images():
	imageFiles = os.listdir("./images/gallery/")
	images = []

	for image in imageFiles:
		if image.endswith(".png"):
			images.append("./images/gallery/" + image)
	return images

def hide_gallery():
	gallery.frame.pack_forget()
	game.frame.pack(side=tk.LEFT)
	
def hide_game():
	game.frame.pack_forget()
	gallery.refresh_gallery(game.matchImages)
	gallery.frame.pack(side=tk.LEFT)

root = tk.Tk()

# Load card images
cardOneImages = load_images()

# Create a menu
menu = tk.Menu(root, borderwidth=2, bg="white")
root.config(menu=menu)

# Add game
game = Game(root, cardOneImages, "./images/back.png")

# Add gallery
gallery = Gallery(root, cardOneImages)
gallery.frame.pack_forget()

# Add menu options
menu.add_command( label="GAME", command=hide_gallery )
menu.add_command( label="GALLERY", command=hide_game )

root.mainloop()

'''
# Create card
cardOne = tk.Button(frame, image=cardOneImages[0])
cardOne.config(command=lambda: switch_img(cardOne, cardOneImages))
cardOne.pack(side=tk.LEFT)

def switch_img (this, imgPair):
	if str(this["image"]) == str(imgPair[0]):
		this.config(image=imgPair[1])
	else:
		this.config(image=imgPair[0])
	
def dummy ():
	print("hey dummy")

'''
