# VTK.wasm for C++ developers

This guide shows you how to compile VTK for WebAssembly, extend the functionality of VTK with your own C++ code and ultimately leverage your
extensions to build 3D web visualization apps.

## Usage patterns

Writing parts of your application in C/C++ allows you to optimize data processing, IO, and rendering. In addition, you can integrate highly
efficient third-party C++ libraries that were traditionally used only outside the browser. There are three approaches when choosing the C/C++
approach for web apps in VTK.

1. [__Embind Simple__](./app-1.md): Write the business logic of your application in C++ and wrap a simple interface to JavaScript with Embind.
2. [__Embind Advanced__](./app-2.md): Audit the VTK classes and only wrap what you need from VTK.
3. [__Plain JavaScript__](./app-3.md): Enable code gen for serdes of C++ classes and initialize a standalone VTK session with your module's serdes registrar functions.
