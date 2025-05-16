# VTK 3D Widgets with VTK.wasm and trame

VTK 3D widgets let you interact with the 3D view in a way that you can drive a processing filter interactively.

In the example below we cover how you can create such widget in plain VTK and how to enable it on the client within the WASM context.

![Clip Plane Widget](/assets/images/trame/clip.png)

The code below highlight some important region and logic to understand.

::: code-group
<<< ../../../examples/trame/widget/clip.py#widget{py:line-numbers=62} [VTK 3D Widget]
<<< ../../../examples/trame/widget/clip.py#trameWidget{py:line-numbers=114} [Trame widget]
<<< ../../../examples/trame/widget/clip.py#trameChange{py:line-numbers=168} [State change]
<<< ../../../examples/trame/widget/clip.py{py:line-numbers} [Full code (clip.py)]
<<< ../../../examples/trame/widget/requirements.txt
:::

## Explanation

If we just focus on the trame integration of a 3D widget for WASM, we realize that there is 3 steps that needs to be followed.

1. First you need to register the widget to `vtklocal.LocalView` instance so the class get instantiated on the client side as well with all its behavior. This is done __line 126__ (`view.register_vtk_object(self.widget)`).
2. Then we need to attach a listener to that widget and bind a trame state to some internal of the vtk objects that is living on the WASM side. For that we rely on the __listener__ property. The listener structure is a set of nested dictionaries where the root keys are the various VTK objects (WASM id of such object) on which you want to bind observers. The second layer is the name of the VTK event you want the system to listen to. The thrid layer is the trame state variable that will be update. Each trame state variable will be a JavaScript object itself where each key will be resolved via some property lookup on the WASM instance. For the final data lookup piece, you need to provide a path to the data you try to extract like the following examples `(wasm_id_of_vtk_object, PropertyName...)`. If you just put the `wasm_id`, you will get the full state of the corresponding vtkObject.
3. Finally, on the trame state side, you need to listen to the variable so you can map to the filter and ask the widget to synchronize its data with the server. 

The [__full working code__](https://github.com/Kitware/vtk-wasm/tree/main/examples/trame/widget) is also available. 