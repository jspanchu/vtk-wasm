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

<<< ../../public/demo/example.js

Result:

<iframe src="/vtk-wasm/demo/plain-javascript.html" style="width: 100%; height: 40vh; border: none;"></iframe>

