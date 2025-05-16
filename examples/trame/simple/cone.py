# Should import classes from vtkmodules
# but as an example we use vtk for simplicity
import vtk

from trame.app import TrameApp
from trame.decorators import change
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3, vtklocal


class Cone(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._setup_vtk()
        self._build_ui()

    def _setup_vtk(self):
        # region vtk
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindow.OffScreenRenderingOn()

        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)
        renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        cone_source = vtk.vtkConeSource()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()
        mapper.SetInputConnection(cone_source.GetOutputPort())
        actor.SetMapper(mapper)
        renderer.AddActor(actor)
        renderer.ResetCamera()
        renderWindow.Render()
        # endregion vtk

        self.render_window = renderWindow
        self.cone = cone_source
        self.actor = actor

    def _build_ui(self):
        with SinglePageLayout(self.server) as layout:
            self.ui = layout

            layout.title.set_text("WASM Cone")
            layout.icon.click = self.ctrl.view_reset_camera

            with layout.toolbar as toolbar:
                toolbar.density = "compact"
                vuetify3.VSpacer()
                vuetify3.VSlider(
                    prepend_icon="mdi-rhombus-split-outline",
                    v_model=("resolution", 6),
                    min=3,
                    max=60,
                    step=1,
                    density="compact",
                    hide_details=True,
                )
                vuetify3.VSlider(
                    prepend_icon="mdi-opacity",
                    v_model=("opacity", 1),
                    min=0,
                    max=1,
                    step=0.01,
                    density="compact",
                    hide_details=True,
                    classes="mr-4",
                )

            with layout.content:
                # region widget
                with vtklocal.LocalView(
                    self.render_window,
                    throttle_rate=20,
                ) as view:
                    self.ctrl.view_update = view.update_throttle
                    self.ctrl.view_reset_camera = view.reset_camera
                # endregion widget

    @change("resolution")
    def on_resolution(self, resolution, **_):
        self.cone.resolution = resolution
        self.ctrl.view_update()

    @change("opacity")
    def on_opacity(self, opacity, **_):
        self.actor.property.opacity = opacity
        self.ctrl.view_update()


def main():
    app = Cone()
    app.server.start()


if __name__ == "__main__":
    main()
