#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from gimpfu import *

def pgulley_demo(img_size):
	img = gimp.Image(img_size, img_size)
	gimp.Display(img)

	l1 = gimp.Layer(img, "1", img_size, img_size)
	img.add_layer(l1)
	gimp.context_set_gradient("Abstract 3")
	pdb.gimp_drawable_edit_gradient_fill(l1, 2, 0, False, 10, 10, True, 0,0, img_size, img_size) 

	l2 = gimp.Layer(img, "2", img_size, img_size)
	img.add_layer(l2)
	gimp.context_set_gradient("Blinds")
	pdb.gimp_drawable_edit_gradient_fill(l2, 3, 0, False, 10, 10, True, 0,0, img_size, img_size) 
	pdb.plug_in_whirl_pinch(img, l2, 100, -0.5,0.5)
	l2.mode = 16
	gimp.Display(img)
	return img


register(
	"pgulley-demo",
	"Generate a demo image",
	"Generate a demo image",
	"pgulley","pgulley","2023",
	"PgulleyDemo",
	"*",
	[
     (PF_INT, "img_size", "size of square image to generate", None)
	],[(PF_IMAGE, '', ', None')],
	pgulley_demo,
	"<Image>/pgulley/"
	)


main()