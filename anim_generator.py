#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from gimpfu import *
from gimpenums import *
import random
from file_names import pp_name
from animation_drivers import PositionDriver, OpacityDriver
from data import index
import os


"""
Ok cool! This works!
I think the next steps:
* abstract the various methods for generating random positions
* animation- certain params get marked in a public list that can get driven by a wrapper object
* More effects - adding kaliedoscopes, warps, color fuckery in a procedural way
* curate options better- maybe some options are contextually more or less interesting? How to structure those choices?
	*ex, some layer modes tend to be more destructive than interesting the closer they are to the top of an image
	*ex, as above, but depending on if a layer is grayscale or rgb
	*ex, some gradient shapes work best with certain position generators


"""


#for now, a hard coded list of options
GradientOptions = ["Abstract 3","Abstract 2","Abstract 1", "Blinds",  "Crown molding", "FG to BG (HSV clockwise hue)"]

GradientShapeOptions = [
	GRADIENT_BILINEAR, GRADIENT_CONICAL_ASYMMETRIC, GRADIENT_CONICAL_SYMMETRIC, GRADIENT_LINEAR, 
	GRADIENT_RADIAL, GRADIENT_SPIRAL_ANTICLOCKWISE, GRADIENT_SPIRAL_CLOCKWISE, GRADIENT_SQUARE
]

ModeOptions = [
	LAYER_MODE_ADDITION, LAYER_MODE_BURN, LAYER_MODE_DIFFERENCE, LAYER_MODE_DIVIDE,LAYER_MODE_EXCLUSION, LAYER_MODE_GRAIN_EXTRACT,
	LAYER_MODE_HARDLIGHT, LAYER_MODE_LINEAR_BURN, LAYER_MODE_LINEAR_LIGHT, LAYER_MODE_LUMA_DARKEN_ONLY, LAYER_MODE_LUMA_LIGHTEN_ONLY,
	LAYER_MODE_MERGE, LAYER_MODE_MULTIPLY, LAYER_MODE_PIN_LIGHT, LAYER_MODE_SCREEN, LAYER_MODE_SUBTRACT, LAYER_MODE_VIVID_LIGHT, 
	LAYER_MODE_LUMINANCE, LAYER_MODE_HSV_VALUE
]


AnimParamOptions = [
	("grad_end.0",PositionDriver), ("grad_end.1",PositionDriver),# ("grad_start.0",PositionDriver), ("grad_start.1",PositionDriver),
	("opacity", OpacityDriver)
]

def keypoints(img_size):
	opts = [0, img_size * .25, img_size*.5, img_size*.75, img_size]
	return [random.choice(opts), random.choice(opts)]



path = "Projects/gimp-gradblend/output/"


class ImageContextManager():
	def __init__(self, img_size, num_layers, name):
		
		self.img_size = img_size
		self.img = gimp.Image(img_size, img_size)
		self.num_layers = num_layers
		self.name = name

		self.path = path+self.name+"/"
		if not os.path.exists(self.path):
			os.makedirs(self.path)

		self.layers = index({i: self.init_layer() for i in range(self.num_layers)})
		[self.render_layer(i, init=True) for i in range(self.num_layers)]


	#abstract the procedure from the rendering
	def init_layer(self):
		r = random.randint(0,self.img_size)
		layer_def = {
			"grad": random.choice(GradientOptions),
			"grad_shape": random.choice(GradientShapeOptions),
			"grad_start": keypoints(self.img_size),
			"grad_end": [r,r],
			"mode": random.choice(ModeOptions),
			"opacity":100.0 #Not nessecarily!
		}
		return layer_def

	def render_layer(self, i, init=False):
		if init:
			layer = gimp.Layer(self.img, str(i), self.img_size, self.img_size)
			self.img.add_layer(layer)
		else:
			layer = self.img.layers[i]
		#reset the layer at every render
		pdb.gimp_drawable_edit_clear(layer)

		l_def = self.layers[i]

		grad = l_def["grad"]
		gimp.context_set_gradient(grad)

		gtype = l_def["grad_shape"]
		start_px, start_py = l_def["grad_start"]
		end_px, end_py = l_def["grad_end"]
		pdb.gimp_drawable_edit_gradient_fill(layer, gtype, 0, False, 10, 10, True, start_px, start_py, end_px, end_py)

		mode = l_def["mode"]
		layer.mode = mode
		opacity = l_def["opacity"]
		opacity = max(0.0, min(opacity, 100.0))
		layer.opacity = opacity

	def render_image(self):
		[self.render_layer(i) for i in range(self.num_layers)]

	def show_image(self):
		gimp.Display(self.img)

	def save(self):
		xcf_name = self.path+self.name+".xcf"
		self.img.filename = xcf_name
		pdb.gimp_xcf_save(0, self.img, None, xcf_name, xcf_name)
		self.img.clean_all()

	def export(self, suffix="0"):
		suffix = str(suffix)
		self.export_name = self.path+self.name+"-"+suffix+".png"
		new_img = pdb.gimp_image_duplicate(self.img)
		new_img.flatten()
		#layer = pdb.gimp_image_merge_visible_layers(new_img, CLIP_TO_IMAGE)
		pdb.gimp_file_save(new_img, new_img.layers[0], self.export_name, '?')
		pdb.gimp_image_delete(new_img)



class ImageAnimator():
	def __init__(self, img_size, num_layers,steps=1000):
		self.img_size = img_size
		self.num_layers = num_layers
		self.name = pp_name()
		self.path = path+self.name+"/"
		self.gif_name = self.path+self.name+".gif"
		self.gif_root_name =  path+"gifs/"+self.name+".gif"

		if not os.path.exists(path+"gifs/"):
			os.makedirs(path+"gifs/")

		self.xcf_name = self.path+self.name+"-gif.xcf"

		self.img = ImageContextManager(img_size, num_layers, self.name)
		self.img.render_image()
		self.img.show_image()
		self.img.save()

		self.step = 0
		self.max_steps = steps

		self.get_drivers()

	#Struggling with abstraction here...
	def get_drivers(self):
		num_drivers = random.randint(1,int(self.num_layers*1.5))
		#pick WITH REPLACEMENT
		anim_layers = [random.choice(range(self.num_layers)) for k in range(num_drivers)]

		self.drivers = []
		ps = []
		for l in anim_layers:
			p, d = random.choice(AnimParamOptions)
			p_string = str(l)+"."+p
			while p_string in ps:
				p, d = random.choice(AnimParamOptions)
				p_string = str(l)+"."+p
			ps.append(p_string)
			start_value = self.img.layers.find(p_string)
			driver = d(start_value, self.img_size, self.max_steps)
			self.drivers.append((p_string, driver))
		

	def export(self):
		self.img.export(suffix=self.step)

	#Super simple animation, just increment one value...
	def take_step(self):
		for param, driver in self.drivers:
			driver.step()
			self.img.layers.assign(param, driver.val)
		self.img.render_image()
		self.export()

	def play(self):
		while self.step < self.max_steps:
			self.take_step()
			self.step += 1
		
	def collate_gif(self):
		self.anim_img = gimp.Image(self.img_size, self.img_size)
		self.anim_img.filename = self.xcf_name
		self.frames = [p for p in os.listdir(self.path) if ".png" in p]

		print("loading "+str(len(self.frames))+" frames")
		self.frames.sort(key=lambda x: int(x.split("-")[1].split(".")[0]))
		for f in self.frames:
			print(self.path+f)
			layer = pdb.gimp_file_load_layer(self.anim_img, self.path+f)
			self.anim_img.add_layer(layer)
		gimp.Display(self.anim_img)
		pdb.gimp_xcf_save(0, self.anim_img, None, self.xcf_name, self.xcf_name)

	def save_gif(self):
		self.collate_gif()
		image = pdb.gimp_image_duplicate(self.anim_img)
		layers = image.layers
		
		pdb.gimp_image_convert_indexed(image, NO_DITHER, MAKE_PALETTE, 256, False, False, "")
		pdb.file_gif_save(image, layers[0], self.gif_name, self.gif_name, 0, 1, 100, 0)
		pdb.file_gif_save(image, layers[0], self.gif_root_name, self.gif_name, 0, 1, 100, 0)

		




def pgulley_animator(img_size, num_layers, steps):
	a = ImageAnimator(img_size, num_layers, steps)	
	a.play()
	a.save_gif()
	return a.img.img



register(
	"pgulley_animator",
	"Generate and animate a procedural demo image",
	"Generate and animate a procedural demo image",
	"pgulley","pgulley","2023",
	"AnimateV2",
	"*",
	[
     (PF_INT, "img_size", "size of square image to generate", 500),
     (PF_INT, "num_layers", "number of layers to generate", 5),
     (PF_INT, "steps", "number of steps to animate", 10)
	],[(PF_IMAGE, '', ', None')],
	pgulley_animator,
	"<Image>/pgulley/"
	)


main()