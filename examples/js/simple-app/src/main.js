import "./style.css";
import { createNamespace } from "@kitware/trame-vtklocal/dist/esm/vtk.mjs";
import { buildWASMScene } from "./example";

createNamespace().then((vtk) => {
  buildWASMScene(vtk, "#app > canvas");
});
