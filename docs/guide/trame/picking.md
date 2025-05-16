# Call to VTK.wasm from Python

VTK 3D widgets let you interact with the 3D view in a way that you can drive a processing filter interactively.

In the example below we cover how you can create such widget in plain VTK and how to enable it on the client within the WASM context.

![Wheel picking](/assets/images/trame/pick1.png)

The code below highlight some important region and logic to understand.

::: code-group
<<< ../../../examples/trame/picking/pick.py#vtk{py:line-numbers=45} [VTK 3D Widget]
<<< ../../../examples/trame/picking/pick.py#trameWidget{py:line-numbers=85} [Trame widget]
<<< ../../../examples/trame/picking/pick.py#trameChange{py:line-numbers=121} [State change]
<<< ../../../examples/trame/picking/pick.py#py2wasmCall{py:line-numbers=130} [Method call]
<<< ../../../examples/trame/picking/pick.py{py:line-numbers} [Full code (pick.py)]
<<< ../../../examples/trame/picking/requirements.txt
:::

| ![Window picking](/assets/images/trame/pick3.png) | ![Full car picking](/assets/images/trame/pick2.png) |
| -- | -- | 

## Hight level explanation

1. Create a vtkPicker and register it so it can be created on the WASM side.
2. Attach a listener on the interactor so you can capture on the server side the picking location (x,y).
3. Call "Pick" on the picker on the WASM side.
4. If something was found, lookup the actor by making another call and convert the result into an actual vtkObject on the server side. 
5. Apply some change on the scene and push the update view to the client.
