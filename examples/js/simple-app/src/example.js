export async function buildWASMScene(
  vtk,
  canvasSelector = "#vtk-wasm-window",
) {
  // Make up some data array to generate a mesh (JS-only)
  function makeQuadMesh(nx, ny) {
    // Create a grid of points on the XY plane from (0, 0) to (nx, ny)
    const pointJSArray = [];
    for (let i = 0; i < ny + 1; i++) {
      for (let j = 0; j < nx + 1; j++) {
        const x = (j - 0.5 * nx) / nx;
        const y = (i - 0.5 * ny) / ny;
        pointJSArray.push(x); // x-coordinate
        pointJSArray.push(y); // y-coordinate
        pointJSArray.push(
          2 * Math.sqrt(x * x + y * y) * Math.sin(x) * Math.cos(y),
        ); // z-coordinate
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
  const polys = vtk.vtkCellArray();
  const connectivity = vtk.vtkTypeInt32Array();
  const offsets = vtk.vtkTypeInt32Array();

  // Ways to bind JS data to VTK.wasm types
  // => method call are async and needs to be awaited
  // => property can be accessed using the dot notation
  await points.data.setArray(new Float32Array(meshData.points));
  await connectivity.setArray(new Int32Array(meshData.connectivity));
  await offsets.setArray(new Int32Array(meshData.offsets));

  // Calling methods with other vtkObject as arguments
  await polys.setData(offsets, connectivity);

  // Using properties to set values as a batch update
  const polyData = vtk.vtkPolyData();
  polyData.set({ points, polys });

  // Getting values from method call (async) or property (sync)
  console.log("NumberOfPoints:", await polyData.getNumberOfPoints());
  console.log("NumberOfCells:", await polyData.getNumberOfCells());
  console.log("PolyDataBounds:", await polyData.getBounds());

  // Create object with properties in constructor
  const mapper = vtk.vtkPolyDataMapper();
  await mapper.setInputData(polyData);
  const actor = vtk.vtkActor({ mapper });

  // Setting a property even across vtkObjects
  // Same as: await (await actor.getProperty()).setEdgeVisibility(true);
  actor.property.edgeVisibility = true;

  // Setup rendering part
  const renderer = vtk.vtkRenderer();
  await renderer.addActor(actor);
  await renderer.resetCamera();

  // Create a RenderWindow and bind it to a canvas in the DOM
  const renderWindow = vtk.vtkRenderWindow({ canvasSelector });
  await renderWindow.addRenderer(renderer);
  const interactor = vtk.vtkRenderWindowInteractor({
    canvasSelector,
    renderWindow,
  });

  // Trigger render and start interactor
  await interactor.render();
  await interactor.start();

  // Observing vtkObject
  const tag = renderWindow.observe("StartEvent", () => {
    console.log("Camera position", renderer.activeCamera.position);
  });
  setTimeout(() => {
    // Remove observer for one specific tag
    renderWindow.unObserve(tag);

    // Remove all observers
    renderWindow.unObserveAll();

    // Print the full state of a vtkObject
    console.log("Camera state:", renderer.activeCamera.state);
  }, 30000);
}
