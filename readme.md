Using the gimp python bindings to generate procedural variations of simple abstractions, by layering gradients together.


Still in exploratory phase

Example manual scripting:

```
 i = gimp.Image(100,100)
 gimp.display(i)
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

 Many idiosyncracies here- managing "modes" which are referred to just by an enum whose values are obscured to me is very annoying
 And editing gradientts is probably really a pain- relying on builtins is fine I guess, to start. 
 
 The basic pattern seems clear to me though: 
 - specify a number of layers
 - for each layer...
 - - specify a gradient and gradient mode
 - - draw that gradient
 - - optionally apply a distorting filter
 - - specify the layer blend mode

The next step will be to architect this so that we can instantiate a given stack from a serialised form... right?
so that we can drive animation of that stack along specified parameters.

Or I guess architect it so that each generation itself is a freezable object which exposes methods to increment parameters?
That feels closer to something like a processing loop- and we can do iterate things interactively. 

