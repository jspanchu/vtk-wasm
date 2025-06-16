## Latest updated

Clipping planes on mapper is now supported. Which allow us to implement that demo in plain client side.

<iframe src="/vtk-wasm/demo/viewer-starfighter2.html" height="592" width="100%" frameborder="0" allowfullscreen="" title="Rendering clipping"></iframe>

## Add support for 32 and 64 bits WASM bundle

....

## Add runtime support for WebGL2 and WebGPU

You can now choose the backend to use for rendering your VTK scene. The WebGPU is still work in progress but is now available for testing via runtime configuration option.

## Helper JavaScript library

A new JavaScript library is available under `@kitware/trame-vtklocal` which delivers a set of helper tools for VTK.wasm and JavaScript.
This include a standalone viewer for a VTK scene dump, a wrapper for pure JavaScript usage and some core handler when creating a widget (i.e. React, Svelt, Angular...) for interating with a trame-vtklocal server implementation.

## API refactor with remote and standalone capabilities

bla

## VTK 9.5 is out

The 9.5 release includes many improvment regarding the integration of WASM. With this new release, on top of observing VTK objects on the client side, you can also perform methods call. This enables us to implement some client/server calls for handling picking with client side resolution. The other hidden improvement is related to the increased number of vtk objects available in WASM which should help in reproducing more complex VTK scene more accurately.
