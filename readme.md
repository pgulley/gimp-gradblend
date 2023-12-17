Using the gimp python bindings to generate procedural variations of simple abstractions, by layering gradients together.


The basic pattern for generating an image is: 
 - specify a number of layers
 - for each layer...
 - - specify a gradient and gradient mode
 - - draw that gradient 
 - - optionally apply a distorting filter
 - - specify the layer blend mode

Example via manual scripting:

```
i = gimp.Image(100,100)
gimp.Display(i)
l = gimp.Layer(i, "1", 100, 100)
i.add_layer(l)
gimp.pdb.gimp_drawable_edit_gradient_fill(l, 2, 0, False, 10, 10, True, 0,0,100,100) 
l2 = gimp.Layer(i, "2", 100, 100)
i.add_layer(l2)
gimp.context_set_gradient("Blinds")
gimp.pdb.gimp_drawable_edit_gradient_fill(l2, 2, 0, False, 10, 10, True, 0,0,100,100) 
l2.mode = 12
gimp.pdb.plug_in_whirl_pinch(i, l2, 100, -0.5,0.5)
 ```

* pgulley_demo
- - Sequentially applies exactly the above script- to generate a demo image

* pgulley_basic_generator
- - Procedurally generates and saves an image based on variations of the above model 

* pgulley_animator_generator
- - abstracts generation from deterministic rendering- so we can change parameters to produce animations

Future:

Ok cool! This works!
I think the next steps:
* more animation options- and sequencing animations?
* More effects - adding kaliedoscopes, warps, color fuckery in a procedural way
* curate parameter options better- maybe some options are contextually more or less interesting? How to structure those choices?
	* ex, some layer modes tend to be more destructive than interesting the closer they are to the top of an image
	* ex, as above, but depending on if a layer is grayscale or rgb
	* ex, some gradient shapes work best with certain position generators

* save and reload python objects- re-run outputs with manual edits



