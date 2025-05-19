# Modern JavaScript development

Modern web development rely on package manager to bring project dependencies. This section covers how published releases can be used within a JavaScript project.

## Project setup

In the simple example we are going to use [Vite](https://vite.dev/) with Vanilla JavaScript. The full code is available for reference [here](https://github.com/Kitware/vtk-wasm/tree/main/examples/js/simple-app).

::: code-group
<<< ../../../examples/js/simple-app/package.json
<<< ../../../examples/js/simple-app/index.html
<<< ../../../examples/js/simple-app/src/main.js [src/main.js]
<<< ../../../examples/js/simple-app/src/example.js [src/example.js]
<<< ../../../examples/js/simple-app/src/style.css [src/style.css]
```bash [Install/Build]
npm install
npm run build
```
:::

Since we are not publishing our WASM bundle to npm yet, we are using the one hosted on our documentation web site under `https://kitware.github.io/vtk-wasm/wasm32/9.5.0/vtkWebAssemblyInterface.mjs`. But you can also download it from our [CI registry](https://gitlab.kitware.com/vtk/vtk/-/packages?orderBy=created_at&sort=desc&search[]=wasm) and serve it or import it yourself.


## Result

<iframe src="/vtk-wasm/demo/simple-app/index.html" style="width: 100%; height: 25vh; border: none;"></iframe>
