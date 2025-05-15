# Plain JavaScript

The following example set rely on loading the `vtk.umd.js` bundle from a CDN.

<iframe src="/vtk-wasm/demo/plain-javascript.html" style="width: 100%; height: 40vh; border: none;"></iframe>

## Defer WASM loading

In this example we rely on the global `vtkWASM` to create our vtk namespace to use in plain JavaScript.
We've also externalized the JS/WASM code as this part don't change.

In this context we provide the URL where the WASM bundle can be found and used from.

::: code-group

<<< ../../public/demo/plain-javascript.html
<<< ../../public/demo/example.js

:::

## Load WASM as module

In this example we pre-load the WASM module and use `vtkWASM` without any URL.

::: code-group

<<< ../../public/demo/preload-plain-javascript.html
<<< ../../public/demo/example.js

:::