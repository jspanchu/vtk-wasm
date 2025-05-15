# VTK.wasm from JavaScript side

While VTK is a comprehensive C++ library, WASM is giving us an opportunity to enable it on servers and clients like your browser. 

In this guide we will focus on how WASM can be used from plain JavaScript without any C++ knowledge and using the WASM bundle generated for our trame needs. 

## Available environment

Web development has many faces between ESM, UMD and plain script usage. Each path is different to some extent so we will cover each of them in their own guide.

- Plain JavaScript usage
- Using modern bundler

## What does it looks like?

Since our WASM bundle is based on our trame needs, it currently mainly focus on the rendering stack (PolyData, Mappers and Actors...) but we plan to extend it with more VTK class coverage down the road. 

So if we ignore how to get your hand on a __vtk__ namespace (see section above), you will be able to write code like below to interact with the available VTK classes in plain JavaScript.

```js
const vtk = [...];

// Make up some data array to generate a mesh (JS-only) 
function makeQuadMesh(nx, ny) {
    // Create a grid of points on the XY plane from (0, 0) to (nx, ny)
    const pointJSArray = []
    for (let i = 0; i < ny + 1; i++) {
        for (let j = 0; j < nx + 1; j++) {
            const x = (j - 0.5 * nx) / nx;
            const y = (i - 0.5 * ny) / ny;
            pointJSArray.push(x); // x-coordinate
            pointJSArray.push(y); // y-coordinate
            pointJSArray.push(5 * Math.sqrt(x * x + y * y) * Math.sin(x) * Math.cos(y)); // z-coordinate
        }
    }

    const connectivityJSArray = [];
    const offsetsJSArray = [];
    for (let i = 0; i < ny; i++) {
        for (let j = 0; j < nx; j++) {
            offsetsJSArray.push(connectivityJSArray.length);
            connectivityJSArray.push(j + i * (nx + 1));
            connectivityJSArray.push(j + i * (nx + 1) + 1);
            connectivityJSArray.push(j + i * (nx + 1) + nx + 2);
            connectivityJSArray.push(j + i * (nx + 1) + nx + 1);
        }
    }
    offsetsJSArray.push(connectivityJSArray.length);

    return { 
        points: pointJSArray, 
        offsets: offsetsJSArray, 
        connectivity: connectivityJSArray,
    };
}
const meshData = makeQuadMesh(50, 50);

// Working on VTK.wasm
// => vtkObject creation is directly available on the vtk namespace
const points = vtk.vtkPoints();
const quads = vtk.vtkCellArray()
const connectivity = vtk.vtkTypeInt32Array();
const offsets = vtk.vtkTypeInt32Array();

// Ways to bind JS data to VTK.wasm types
// => method call are async and needs to be awaited
// => property can be accessed using the dot notation
await points.Data.SetArray(new Float32Array(mesh.points));
await connectivity.SetArray(new Int32Array(mesh.connectivity));
await offsets.SetArray(new Int32Array(mesh.offsets));

// Calling methods with other vtkObject as arguments
await quads.SetData(offsets, connectivity);

// Using properties to set values as a batch update
const polyData = vtk.vtkPolyData();
polyData.set({
    Points: points,
    Polys: quads,
})

// Getting values from method call (async) or property (sync)
console.log("NumberOfPoints:", await polyData.GetNumberOfPoints()); 
console.log("NumberOfCells:", await polyData.GetNumberOfCells());
console.log("PolyDataBounds:", polyData.Bounds);

// Create object with properties in constructor
const mapper = vtk.vtkPolyDataMapper();
await mapper.SetInputData(polyData);
const actor = vtk.vtkActor({ Mapper: mapper });

// Setting a property even across vtkObjects
// Same as: await (await actor.GetProperty()).SetEdgeVisibility(true);
actor.Property.EdgeVisibility = true;

// Setup rendering part
const renderer = vtk.vtkRenderer();
await renderer.AddActor(actor);
await renderer.ResetCamera();

// Create a RenderWindow and bind it to a canvas in the DOM
const wasmCanvasSelector = "#vtk-wasm-window";
const renderWindow = vtk.vtkRenderWindow({ 
    CanvasSelector: wasmCanvasSelector,
});
await renderWindow.AddRenderer(renderer);
const interactor = vtk.vtkRenderWindowInteractor({ 
    CanvasSelector: wasmCanvasSelector, 
    RenderWindow: renderWindow,
});

// Trigger render and start interactor
await interactor.Render();
await interactor.Start();

// Observing vtkObject
const tag = renderWindow.observe("StartEvent", () => {
    console.log("Camera position", renderer.ActiveCamera.Position);
});
setTimeout(() => {
    // Remove observer for one specific tag
    renderWindow.unObserve(tag);

    // Remove all observers
    renderWindow.unObserveAll();

    // Print the full state of a vtkObject
    console.log("Camera state:", renderer.ActiveCamera.state);
}, 30000);
```

Result:

<iframe src="/vtk-wasm/demo/plain-javascript.html" style="width: 100%; height: 40vh; border: none;"></iframe>

