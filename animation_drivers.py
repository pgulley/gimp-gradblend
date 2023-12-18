#Helpers to drive animation parameters
import math
import random
"""
#We'll have some funny composite classes here
Want to animate: 
	points
	opacity



"""

class Linear():
	def __init__(self, start, rate):
		self.start_value = start
		self.val = start
		self.rate = rate
		self.i = 0

	def step(self):
		self.i += 1
		self.val  = self.start_value + (self.i*self.rate)


class SineWave():
	def __init__(self, start, rate, amplitude):
		self.start_value = start
		self.val = start
		self.rate = rate
		self.amplitude = amplitude

		self.step_size = math.pi / rate

		self.i = 0

	def step(self):
		self.i += 1
		self.val = self.start_value + self.amplitude*math.sin(self.step_size*self.i)

class CosineWave():
	def __init__(self, start, rate, amplitude, clamp=False):
		self.start_value = start
		self.val = start
		self.rate = rate
		self.amplitude = amplitude

		self.step_size = math.pi / rate

		self.i = 0

	def step(self):
		self.i += 1
		self.val = self.start_value + self.amplitude*math.cos(self.step_size*self.i)


class RandomRamp():
	def __init__(self, start, full_loop_duration, hold = 0):
		self.start_value = start
		self.val = start
		self.hold = hold
		self.ramp_rate = 5 
		self.ramp_down = random.randint(0, full_loop_duration//2)

		self.ramp_up = random.randint(full_loop_duration//2, int(full_loop_duration*.9))

		self.i = 0
	
	def step(self):

		if self.i > self.ramp_down and self.i <self.ramp_up and self.val > self.hold:
			self.val  = self.start_value - ((self.i-self.ramp_down)*self.ramp_rate)

		if self.i > self.ramp_up and self.val < self.start_value:
			self.val = self.hold + ((self.i - self.ramp_up)*self.ramp_rate)


def PositionDriver(start_value, img_size, full_loop_duration):
	#Let everything loop
	opt = random.choice(["sin"])
	if opt == "lin":
		rate = random.choice([1,1,1,1,2,2,4,4,4,8,8])
		return Linear(start_value, rate)

	if opt == "sin":
		loops = random.choice([1,1,1,2,2,2,2,4,4,5])
		rate = full_loop_duration / loops
		amplitude = random.randint(img_size//2, int(img_size*1.5))
		return SineWave(start_value, rate, amplitude)



def OpacityDriver(start_value, img_size, full_loop_duration):

	opt = random.choice(["cos", "ramp"])
	if opt == "cos":
		loops = random.choice([1,1,1,1,2,2,2,3,3,4])
		rate = full_loop_duration / loops
		if start_value == 0:
			amplitude = 100
		else:
			amplitude = -100
		return CosineWave(start_value, rate, amplitude)
	
	if opt == "ramp":
		return RandomRamp(start_value, full_loop_duration)
