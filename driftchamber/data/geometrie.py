class Cell():
	def __init__(self,  position ):
		self.deposited_energy=0
		self.triggered = False
		self.pos = position				#in (x, y) - Tupel
		#self.size = 1					#given in UserStory, not sure if necessary

	def deposit_energy(self,energy):
		self.triggered=True
		self.deposited_energy += energy

	def been_hit(self):
		return self.triggered

	def print_info(self):
		'''
		Returns all information necessary for printing
		'''
		return (self.position, self.triggered)

	def energy(self):
		return self.deposited_energy

class Layer():
	def __init__(self, width, lines, position_y=0 ):
		self.pos = postition				#lower left corner of detectorarray
		self.width = width				#Amount of cells per line
		self.stack = lines				#Amount of stacked cell_lines

		self.cells = []					#Generate all cells for Layer
		for s in range(self.stack):
			line = []
			for l in range(self.width):
				tmp = Cell( postition = self.pos + (l, s)  )#postition = layer_offset + l-th cell
				line.append(tmp)
			self.cells.append(line)
								#self.cells = [ line1, line2, ... ]
								#lineX = [cell1, cell2, ...]

class SuperLayer():
	def __init__(self, width, layers ):
		'''
		width INT total width of detector
		layers INT
		'''
		self.width = width
		
		self.layers = []
		for i, size in enumerate(layer_sizes):
			self.layers.append( Layer(self.width, lines=size, position=i ) )
								#self.layers = [layer1, layer2, ... ]


	
class detector():
	def __init__(self, width, superlayers, layer_info ):
		'''
		Create detector
		with 'superlayers' amount of Superlayers
		and for each Superlayer the amount of layers
		'''
		pass

	def deposit_energy_at(self, pos):	#position as (x,y)
		'''
		deposits energy at the cell at position (x,y)
		'''
		pass
		
	def print(self):
		'''
		Insert Code to print the detector cells
		Position of this function will probaly changPosition of this function will probaly change
		'''
		pass
