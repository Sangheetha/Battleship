#Battleship Game

ship_length_dict = {"Aircraft Carrier":5,"Battleship": 4,"Submarine":3,"Destroyer":3,"Patrol Boat":2}
ship_abbrev_dict = {"A":0,"B":1,"S":2,"D":3,"P":4}


def Game():
	#TODO: Write code for this function
	"""plays out a game of Battleship between two users, keeping score"""
	BOARDROWS = 10
	BOARDCOLUMNS = 10


	player1Board = Board(BOARDROWS,BOARDCOLUMNS)
	print "--------------BATTLESHIP (Player 1 V.S. Player 2)-------------"
	print "Welcome to Battleship, Player 1!" 
	print "You will now place your ships on the board. Choose wisely"

	player1ships = player1Board.FillBoard("Player 1")


class Board:

	def __init__(self,rows, columns):
		"""initializes the board class"""
		self.data = [[' ' for i in range(columns)] for j in range(rows)] 
		self.row = rows
		self.col = columns 

		ac = Ship("Aircraft Carrier", self)
		bs = Ship("Battleship",self)
		d = Ship("Destroyer",self)
		s = Ship("Submarine",self)
		p1 = Ship("Patrol Boat",self)
		self.ships = [ac,bs,d,s,p1] 
		self.shipsCount = 5

	def __repr__(self):
		s = "  "
		for col  in range(self.col):
			s += "|" + chr(65+col)  #Prints top row of ' A B C D'
		s += "|\n"

		for row in range(self.row):
			s += "---" + self.col*"--" + "\n" 
			s += str(row+1)  #Prints left column of "1 2 3 4 5"
			if row < 9:
				s+= " "
			s += "".join(["|" + self.data[row][col] for col in range(self.col)]) 
			s += "|\n" 


		return s 

	def clear(self):
		"""empties the board of ships"""
		for row in range(self.row):
			for col in range(self.col):
				self.data[row][col] = " "

	def placeShip(self,ship):	
		"""places a ship on the game board""" 
		startrow = ship.pos[0]
		startcol = ship.pos[1]
		if ship.orient == "H":
			self.data[startrow][startcol:startcol+ship.len] = [ship.type[0]]*ship.len 
		elif ship.orient == "V":
			for i in range(ship.len):
				self.data[startrow+i][startcol] = ship.type[0]

	def userFillBoard(self,player):
		"""lets a user place their ships on the board"""
		print
		print self

		for ship in self.ships:
			print "You will now place the",ship.type,"on the board."
			print "It is",ship.len,"squares long."
			ship.userPlaceShip()
			print 
			print self

		
	def userFireOne(self,player,fake):
		"""lets a user fire one missile at the board, and lets them know if it was a hit or miss"""
		print "You can now fire a missile at your opponents board, " + player + "."
		userchoice = raw_input("> ")
		rowchoice = int(userchoice[1:])-1
		colchoice = ord(userchoice[0]) - 65

		#Handles cases where grid square has already been hit or is not on board
		while fake.data[rowchoice][colchoice] in ['X', 'O'] or rowchoice > self.row or colchoice > self.col:
			print "That is not a valid choice. Please pick again."
			print
			print fake
			userchoice = raw_input("> ")
			rowchoice = int(userchoice[1:]) - 1
			colchoice = ord(userchoice[0]) - 65

		#Hit no boats
		if self.data[rowchoice][colchoice] == " ":
			fake.data[rowchoice][colchoice] = 'O'
			print fake
			print
			print "You missed! Better luck next time."
			print

		#Hit a boat
		else:
			abbrev = self.data[rowchoice][colchoice]
			hitship = self.ships[ship_abbrev_dict[abbrev]]
			sunk = hitship.gotHit(rowchoice,colchoice)  
			fake.data[rowchoice][colchoice] = 'X'
			print fake
			print
			if not sunk: 
				print "You hit a ship!"
			print 



	def userFireBoard(self,player):
		#TODO: Test this function
		"""lets a user fire missiles at a board, lets them know when they have hit a ship. returns number of shots
		taken to hit all ships"""

		playerhits = 0 
		fakeboard = Board(10,10)
		print fakeboard

		while self.shipsCount != 0:
			print 
			self.userFireOne(player, fakeboard)

		print "You have eliminated all ships on the board!"
		return


class Ship: 

	def __init__(self,shiptype, board):
		self.len = ship_length_dict[shiptype]
		self.type = shiptype
		self.b = board  
		self.orient = self.initOrientPos()[1] 
		self.pos = self.initOrientPos()[0]
		self.hits = [False]*self.len


	def __repr__(self):
		s = "The Ship Properties\n"
		s += "\tLength: " + str(self.len) +"\n"
		s += "\tOrientation: " + str(self.orient) + "\n"
		s += "\tPosition: " + str(self.pos) + "\n"
		return s 

	def initOrientPos(self):
		"""finds an initial empty position and orientation for the ship to be
		 defaults to horizontal"""
		for row in range(self.b.row):
			for col in range(self.b.col):
				if self.b.data[row][col:col+self.len] == [" "]*self.len:
					return [(row, col),"H"]
		#can't find empty space in horizontal orientation, search vertically
		for col in range(self.b.col):
			for row in range(self.b.row):
				p = []  #Potential space for ship 
				for i in range(self.len):
					p += [self.b.data[row+i][col]]
				if p == [" "]*self.len:
					return [(row,col),"V"]
		return ["NP","NP"] #Nowhere to place ship 

	def allowPos(self):
		"""returns True if ship's position is allowed on the board, returns false
		otherwise"""
		startrow = self.pos[0]
		startcol = self.pos[1]

		if self.orient == "H":
			if self.b.data[startrow][startcol:startcol+self.len] == [" "]*self.len:
				return True
			else:
				return False 

		if self.orient == "V":
			gridspace = [] 
			for i in range(self.len):
				gridspace += self.b.data[startrow+i][startcol]
			if gridspace == [" "]*self.len:
				return True
			else:
				return False 

	def userPlaceShip(self):
		"""places a ship based on the user's input"""
		print "What orientation should be the ship be in?"		
		print "\t(1) Horizontal"
		print "\t(2) Vertical"
		orientation = input("> ")
		while orientation != 1 and orientation != 2:
			print "That is not a valid choice. Try again."
			orientation = input(">")

		if orientation == 1:
			self.orient = "H"
		elif orientation == 2:
			self.orient = "V"
		print 

		print "Give the position for the ship."
		position = raw_input("> ")
		rowpos = int(position[1]) - 1
		colpos = ord(position[0]) - 65 
		self.pos = (rowpos,colpos)	

		while not self.allowPos() or position < 2:
			print "That is not a valid place to put a ship. Try again."
			print 
			print "What orientation should be the ship be in?"		
			print "\t(1) Horizontal"
			print "\t(2) Vertical"
			orientation = input("> ")
			while orientation != 1 and orientation != 2:
				print "That is not a valid choice. Try again."
				orientation = input(">")

			if orientation == 1:
				self.orient = "H"
			elif orientation == 2:
				self.orient = "V"
			print 

			print "Give the position for the ship."
			position = raw_input("> ")
			rowpos = int(position[1:]) - 1
			colpos = ord(position[0]) - 65 
			self.pos = (rowpos,colpos)	

		self.b.placeShip(self)

	def gotHit(self,row,col):
		"""adjusts variables when ship gets hit, returns True if ship hit"""

		#Horizontal Ship
		if self.orient == "H":
			hitindex = col-self.pos[1]
			self.hits[hitindex] = True
			if False not in self.hits:
				print "Your opponent's " + self.type + " has been sunk!"
				print
				self.b.shipsCount += -1
				return True
			else:
				return False

		#Vertical Ship
		if self.orient == "V":
			hitindex = row-self.pos[0]
			self.hits[hitindex] = True
			if False not in self.hits:
				print "Your opponent's " + self.type + " has been sunk!"
				print
				self.b.shipsCount += -1
				return True
			else:
				return False
