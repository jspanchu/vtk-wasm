# Should import classes from vtkmodules
# but as an example we use vtk for simplicity
import vtk

from pathlib import Path

from trame.app import TrameApp, asynchronous
from trame.decorators import change
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vuetify3, vtklocal

DATA_PATH = Path(__file__).with_name("data").resolve()

RND_SEQ = vtk.vtkMinimalStandardRandomSequence()
RND_SEQ.SetSeed(8775070)


def next_color():
    rgb = []
    for _ in range(3):
        rgb.append(RND_SEQ.GetRangeValue(0.4, 1.0))
        RND_SEQ.Next()
    return rgb


def apply_settings(property):
    property.diffuse_color = next_color()
    property.diffuse = 0.8
    property.specular = 0.5
    property.specular_color = (1, 1, 1)
    property.specular_power = 30


class Pick(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._picking_prending = False
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

        for file in DATA_PATH.glob("*.vtp"):
            reader = vtk.vtkXMLPolyDataReader(file_name=str(file.resolve()))
            mapper = vtk.vtkPolyDataMapper()
            reader >> mapper
            actor = vtk.vtkActor(mapper=mapper)
            renderer.AddActor(actor)
            apply_settings(actor.property)

        renderer.ResetCamera()
        renderWindow.Render()

        self.picker = vtk.vtkPropPicker()

        self.interactor = renderWindowInteractor
        self.last_picked_actor = None
        self.last_picked_property = vtk.vtkProperty()
        self.renderer = renderer
        self.render_window = renderWindow
        # endregion vtk

    def _build_ui(self):
        with VAppLayout(self.server) as layout:
            self.ui = layout

            vuetify3.VBtn(
                icon="mdi-crop-free",
                click=self.ctrl.view_reset_camera,
                style="top:1rem;right:1rem;z-index:1;position:absolute;",
            )

            # region trameWidget
            with vtklocal.LocalView(
                self.render_window,
                throttle_rate=20,
                ctx_name="wasm_view",  # attach widget on ctx
            ) as view:
                self.ctrl.view_update = view.update_throttle
                self.ctrl.view_reset_camera = view.reset_camera

                # ---------------------------------------------------------
                # Picker handling
                # ---------------------------------------------------------

                # => push picker to client
                view.register_vtk_object(self.picker)
                view.register_vtk_object(self.last_picked_property) # for pure client edit

                # => attach interactor listener
                wasm_interactor_id = view.get_wasm_id(self.interactor)
                view.listeners = (
                    "wasm_listeners",
                    {
                        wasm_interactor_id: {
                            "LeftButtonPressEvent": {  # LeftButtonPressEvent, MouseMoveEvent
                                "clicked_pos": {
                                    "x": (wasm_interactor_id, "EventPosition", 0),
                                    "y": (wasm_interactor_id, "EventPosition", 1),
                                },
                            },
                        },
                    },
                )
                # => reserve state variable for widget update
                self.state.clicked_pos = None
            # endregion trameWidget

    # region trameChange
    @change("clicked_pos")
    def on_click(self, clicked_pos, **_):
        if clicked_pos is None:
            return

        if not self._picking_prending:
            asynchronous.create_task(self._pick_actor(**clicked_pos))

    # endregion trameChange

    # region py2wasmCall
    async def _pick_actor(self, x, y):
        if self._picking_prending:
            return

        self._picking_prending = True
        # Trigger a pick on client
        picked_worked = await self.ctx.wasm_view.invoke(
            self.picker, "Pick", (x, y, 0), self.renderer
        )
        if not picked_worked:
            self._picking_prending = False
            return

        # Restore previous state
        if self.last_picked_actor:
            self.last_picked_actor.property.DeepCopy(self.last_picked_property)
            self.last_picked_actor = None

        actor_info = await self.ctx.wasm_view.invoke(self.picker, "GetActor")
        actor = self.ctx.wasm_view.get_vtk_obj(actor_info.get("Id"))
        actor_prop = actor.property

        # Save current state and capture picked actor
        self.last_picked_property.DeepCopy(actor_prop)
        self.last_picked_actor = actor

        # Highlight actor
        actor_prop.color = (1, 0, 1)
        actor_prop.EdgeVisibilityOn()

        # Render
        self.ctx.wasm_view.update()
        self._picking_prending = False

        # endregion py2wasmCall


def main():
    # region export
    import sys

    app = Pick()
    if "--export" in sys.argv:
        app.ctx.wasm_view.save("porsche.wazex")
        # Print ids
        print(f"render_window:", app.ctx.wasm_view.get_wasm_id(app.render_window))
        print(f"renderer:", app.ctx.wasm_view.get_wasm_id(app.renderer))
        print(f"property:", app.ctx.wasm_view.get_wasm_id(app.last_picked_property))
        print(f"picker:", app.ctx.wasm_view.get_wasm_id(app.picker))
        print(f"interactor:", app.ctx.wasm_view.get_wasm_id(app.interactor))

    app.server.start()
    # endregion export


if __name__ == "__main__":
    main()
