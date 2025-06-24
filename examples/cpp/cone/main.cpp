#include "vtkActor.h"
#include "vtkCallbackCommand.h"
#include "vtkConeSource.h"
#include "vtkNew.h"
#include "vtkPolyData.h"
#include "vtkPolyDataMapper.h"
#include "vtkProperty.h"
#include "vtkRenderWindow.h"
#include "vtkRenderWindowInteractor.h"
#include "vtkRenderer.h"

#include "vtkWebAssemblyOpenGLRenderWindow.h"
#include "vtkWebAssemblyRenderWindowInteractor.h"
#include "vtkWebAssemblyWebGPURenderWindow.h"

#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>

#include <emscripten/bind.h>

namespace {
vtkConeSource *coneSource = nullptr;
vtkRenderWindow *renderWindow = nullptr;
} // namespace

// region emscriptenKeepalive
extern "C" {
EMSCRIPTEN_KEEPALIVE void setConeResolution(int resolution) {
  if (coneSource) {
    coneSource->SetResolution(resolution);
  } else {
    std::cerr << "Error: Cone source is not initialized." << std::endl;
  }
}
}
// endregion emscriptenKeepalive

// region embindFunctions
void setConeHeight(double height) {
  if (coneSource) {
    coneSource->SetHeight(height);
  } else {
    std::cerr << "Error: Cone source is not initialized." << std::endl;
  }
}

void render() {
  if (renderWindow) {
    renderWindow->Render();
  } else {
    std::cerr << "Error: Render window is not initialized." << std::endl;
  }
}

EMSCRIPTEN_BINDINGS(cone_module) {
  emscripten::function("setConeHeight", &setConeHeight);
  emscripten::function("render", &render);
}
// endregion embindFunctions

int main(int argc, char *argv[]) {
  // region args
  int coneResolution = 6;
  std::string canvasSelector = "#canvas";

  for (int i = 0; i < argc; ++i) {
    if (argv[i] && !strcmp(argv[i], "--help")) {
      std::cout
          << "Usage: " << argv[0]
          << " [options]\n"
             "Options:\n"
             "  --help: Show this help message\n"
             "  --resolution: Set the resolution of the cone (default is 6)\n"
             "  --canvas-selector: Set the selector for canvas (default is "
             "#canvas)\n";
      return 0;
    } else if (argv[i] && !strcmp(argv[i], "--resolution")) {
      // Handle resolution option
      if (++i < argc) {
        coneResolution = atoi(argv[i]);
      }
    } else if (argv[i] && !strcmp(argv[i], "--canvas-selector")) {
      if (++i < argc) {
        canvasSelector = argv[i];
      }
    }
  }
  // endregion args
  // region vtk
  // Create pipeline
  coneSource = vtkConeSource::New();
  coneSource->SetResolution(coneResolution);

  vtkNew<vtkPolyDataMapper> mapper;
  mapper->SetInputConnection(coneSource->GetOutputPort());

  vtkNew<vtkActor> actor;
  actor->SetMapper(mapper);
  actor->GetProperty()->SetEdgeVisibility(1);
  actor->GetProperty()->SetEdgeColor(1, 0, 1);

  // Create a renderer, render window, and interactor
  vtkNew<vtkRenderer> renderer;
  renderer->SetBackground(0.2, 0.3, 0.4);
  renderer->AddActor(actor);

  renderWindow = vtkRenderWindow::New();
  renderWindow->AddRenderer(renderer);

  vtkNew<vtkRenderWindowInteractor> renderWindowInteractor;
  renderWindowInteractor->SetRenderWindow(renderWindow);
  renderer->ResetCamera();
  // endregion vtk
  // region bindCanvas
  if (auto *wasmInteractor = vtkWebAssemblyRenderWindowInteractor::SafeDownCast(
          renderWindowInteractor)) {
    // If using WebAssembly, set the canvas selector
    wasmInteractor->SetCanvasSelector(canvasSelector.c_str());
  }

  // If your canvas has id="canvas", this if block is not needed.
  // you can set it here if your canvas has a different id.
  if (auto *webGLRenderWindow =
          vtkWebAssemblyOpenGLRenderWindow::SafeDownCast(renderWindow)) {
    // If using WebAssembly, set the canvas selector
    webGLRenderWindow->SetCanvasSelector(canvasSelector.c_str());
  } else if (auto *webGPURenderWindow =
                 vtkWebAssemblyWebGPURenderWindow::SafeDownCast(renderWindow)) {
    // If using WebGPU, set the canvas selector
    webGPURenderWindow->SetCanvasSelector(canvasSelector.c_str());
  } else {
    // If not using WebAssembly or WebGPU, print an error message
    std::cerr << "Error: Unsupported render window type. "
              << "Please use a WebAssembly or WebGPU render window."
              << std::endl;
    return EXIT_FAILURE;
  }
  // endregion bindCanvas
  // region coneSourceLifecycle
  // Clean up the cone source when the interactor is deleted
  vtkNew<vtkCallbackCommand> onDeleteCallback;
  onDeleteCallback->SetCallback(
      [](vtkObject *caller, unsigned long, void *, void *) {
        if (coneSource != nullptr) {
          coneSource->Delete();
          coneSource = nullptr;
        }
        if (renderWindow != nullptr) {
          renderWindow->Delete();
          renderWindow = nullptr;
        }
      });
  renderWindowInteractor->AddObserver(vtkCommand::DeleteEvent,
                                      onDeleteCallback);
  // endregion coneSourceLifecycle
  // region interactor
  // Start event loop
  renderWindow->Render();
  renderWindowInteractor->Start();
  // endregion interactor
  return EXIT_SUCCESS;
}
