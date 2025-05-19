# Call to VTK.wasm from Python

This example capture the usage of a vtkPiker and illustate the usage of method call from Python.

![Wheel picking](/assets/images/trame/pick1.png)

The code below highlight some important region and logic to understand.

::: code-group
<<< ../../../examples/trame/picking/pick.py#vtk{py:line-numbers=42} [VTK Setup]
<<< ../../../examples/trame/picking/pick.py#trameWidget{py:line-numbers=82} [Trame widget]
<<< ../../../examples/trame/picking/pick.py#trameChange{py:line-numbers=118} [State change]
<<< ../../../examples/trame/picking/pick.py#py2wasmCall{py:line-numbers=129} [Method call]
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

The [__full working code__](https://github.com/Kitware/vtk-wasm/tree/main/examples/trame/picking) is also available. 