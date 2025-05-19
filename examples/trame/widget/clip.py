# Should import classes from vtkmodules
# but as an example we use vtk for simplicity
import vtk

from pathlib import Path

from trame.app import TrameApp
from trame.decorators import change
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3, vtklocal

DATA_PATH = str(Path(__file__).with_name("star-fighter.vtp").resolve())


class Clip(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._setup_vtk()
        self._build_ui()

    def _setup_vtk(self):
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindow.OffScreenRenderingOn()

        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)
        renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        reader = vtk.vtkXMLPolyDataReader(file_name=DATA_PATH)
        bounds = reader().GetBounds()

        plane = vtk.vtkPlane(
            origin=(
                0.5 * (bounds[0] + bounds[1]),
                0.5 * (bounds[2] + bounds[3]),
                0.5 * (bounds[4] + bounds[5]),
            )
        )

        clipper = vtk.vtkClipDataSet(clip_function=plane)
        geometry = vtk.vtkDataSetSurfaceFilter()

        ctx_mapper = vtk.vtkPolyDataMapper()
        reader >> ctx_mapper

        clip_mapper = vtk.vtkPolyDataMapper()
        reader >> clipper >> geometry >> clip_mapper

        clip_actor = vtk.vtkActor(mapper=clip_mapper)
        renderer.AddActor(clip_actor)

        ctx_actor = vtk.vtkActor(mapper=ctx_mapper)
        renderer.AddActor(ctx_actor)
        ctx_actor.property.opacity = 0.1

        renderer.ResetCamera()
        renderWindow.Render()

        # region widget
        # Widget setup
        rep = vtk.vtkImplicitPlaneRepresentation(
            place_factor=1.25,
            outline_translation=False,
        )
        rep.DrawPlaneOff()
        rep.PlaceWidget(bounds)
        rep.normal = plane.normal
        rep.origin = plane.origin

        plane_widget = vtk.vtkImplicitPlaneWidget2(
            interactor=renderWindowInteractor, representation=rep
        )
        plane_widget.On()
        # endregion widget

        self.plane = plane
        self.render_window = renderWindow
        self.actor = clip_actor
        self.ctx_actor = ctx_actor
        self.widget = plane_widget

    def _build_ui(self):
        with SinglePageLayout(self.server) as layout:
            self.ui = layout

            layout.title.set_text("WASM Widget")
            layout.icon.click = self.ctrl.view_reset_camera

            with layout.toolbar as toolbar:
                toolbar.density = "compact"
                vuetify3.VSpacer()
                vuetify3.VCheckbox(
                    true_icon="mdi-eye-outline",
                    false_icon="mdi-eye-off-outline",
                    v_model=("show_ctx", True),
                    hide_details=True,
                    density="compact",
                )
                vuetify3.VSlider(
                    prepend_icon="mdi-opacity",
                    v_model=("opacity", 1),
                    min=0,
                    max=1,
                    step=0.01,
                    density="compact",
                    hide_details=True,
                    classes="mr-6",
                )

            with layout.content:
                # region trameWidget
                with vtklocal.LocalView(
                    self.render_window,
                    throttle_rate=20,
                    ctx_name="wasm_view",
                ) as view:
                    self.ctrl.view_update = view.update_throttle
                    self.ctrl.view_reset_camera = view.reset_camera

                    # ---------------------------------------------------------
                    # Widget handling
                    # ---------------------------------------------------------

                    # => push widget to client
                    wasm_id = view.register_vtk_object(self.widget)

                    # => attach listener to widget and bind data to state
                    view.listeners = (
                        "listeners",
                        {
                            wasm_id: {
                                "InteractionEvent": {
                                    "plane_widget": {
                                        "origin": (
                                            wasm_id,
                                            "WidgetRepresentation",
                                            "Origin",
                                        ),
                                        "normal": (
                                            wasm_id,
                                            "WidgetRepresentation",
                                            "Normal",
                                        ),
                                    },
                                },
                            },
                        },
                    )

                    # => reserve state variable for widget update
                    self.state.plane_widget = None

    # endregion trameWidget

    @change("show_ctx")
    def on_show_ctx(self, show_ctx, **_):
        self.ctx_actor.visibility = show_ctx
        self.ctrl.view_update()

    @change("opacity")
    def on_opacity(self, opacity, **_):
        self.actor.property.opacity = opacity
        self.ctrl.view_update()

    # region trameChange
    @change("plane_widget")
    def on_plane_widget(self, plane_widget, **_):
        if plane_widget is None:
            return

        origin = plane_widget.get("origin")
        normal = plane_widget.get("normal")

        self.plane.SetOrigin(origin)
        self.plane.SetNormal(normal)

        self.ctrl.view_update()

    # endregion trameChange


def main():
    # region export
    import sys

    app = Clip()
    if "--export" in sys.argv:
        app.ctx.wasm_view.save("star-fighter.wazex")

    app.server.start()
    # endregion export


if __name__ == "__main__":
    main()
