# VTK.wasm

VTK.wasm lets you build new, or port existing VTK C++ applications to the web!

[WebAssembly](https://webassembly.org/) (abbreviated Wasm) is a binary instruction format intended to be executed in a virtual machine, for example in a web browser. 

With VTK.wasm, you can distribute your application as a web application that runs in a browser sandbox. This approach is suitable for web distributed applications that do not require full access to host device capabilities.

Guides tailored for different developer backgrounds and needs:
  - **C++ Developers:** Learn to build and port VTK applications to the web using WASM, CMake, and C++.
  - **JavaScript Developers:** Use pre-built WASM bundles to create 3D scenes directly from JavaScript.
  - **Python Developers (trame):** Leverage VTK.wasm rendering capabilities in Python with trame, no C++ or JavaScript required.

Pre-requisite knowledge:
- For general VTK usage, refer to the official [VTK documentation](https://vtk.org/).
- For CMake, we strongly recommed the [CMake Tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/index.html).

The available guides won't cover VTK in general and will only use "simple VTK code" to demonstrate the usage of VTK in the WASM context relevant for your use case. For pure VTK questions, you should refer to the [examples website](https://examples.vtk.org/site/), [VTK API](https://vtk.org/doc/nightly/html/index.html) or the main [VTK website](https://vtk.org/).
