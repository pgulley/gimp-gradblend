#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from gimpfu import *
from gimpenums import *
import random
from file_names import pp_name
import os

"""
Ok cool! This works!
I think the next steps:
* naming and saving images
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


path = "Projects/gimp-gradblend/output/"

class GradGenerator():
	def __init__(self, img_size, num_layers):
		
		self.img_size = img_size
		self.img = gimp.Image(img_size, img_size)
		self.num_layers = num_layers
		self.name = pp_name()
		self.path = path+self.name
		if not os.path.exists(self.path):
			os.makedirs(self.path)


	def make_layer(self):
		layer = gimp.Layer(self.img, "1", self.img_size, self.img_size)
		self.img.add_layer(layer)
		#Select random gradient color
		grad = random.choice(GradientOptions)
		gimp.context_set_gradient(grad)

		#Select a random gradient type
		gtype = random.choice(GradientShapeOptions)

		#gradient will start at a random diagonal pos
		start_p = random.choice([0, self.img_size * .25, self.img_size*.5, self.img_size*.75, self.img_size])

		#may want to situationally restrict this to interesting ranges based on gtype, but that's a later problem
		end_p = random.randint(0,self.img_size)

		#Do the damn thing
		pdb.gimp_drawable_edit_gradient_fill(layer, gtype, 0, False, 10, 10, True, start_p, start_p, end_p, end_p)

		#Pick layer mode
		mode = random.choice(ModeOptions)
		layer.mode = mode

	def generate(self):
		for l in range(self.num_layers):
			self.make_layer()

		gimp.Display(self.img)


	def save(self):
		xcf_name = self.path+"/"+self.name+".xcf"
		self.img.filename = xcf_name
		pdb.gimp_xcf_save(0, self.img, None, xcf_name, xcf_name)

	def export(self):
		self.export_name = self.path+"/"+self.name+".png"
		new_img = pdb.gimp_image_duplicate(self.img)
		layer = pdb.gimp_image_merge_visible_layers(new_img, CLIP_TO_IMAGE)
		pdb.gimp_file_save(new_img, layer, self.export_name, '?')
		pdb.gimp_image_delete(new_img)


def pgulley_basic_generator(img_size, num_layers):
	g = GradGenerator(img_size, num_layers)
	g.generate()
	g.save()
	g.export()
	return g.img



register(
	"pgulley_basic_generator",
	"Generate a procedural demo image",
	"Generate a procedural demo image",
	"pgulley","pgulley","2023",
	"GenDemo",
	"*",
	[
     (PF_INT, "img_size", "size of square image to generate", 500),
     (PF_INT, "num_layers", "number of layers to generate", 5)
	],[(PF_IMAGE, '', ', None')],
	pgulley_basic_generator,
	"<Image>/New/"
	)


main()