from pathlib import Path

from fastapi import FastAPI
from nicegui import app, ui

from make24_solver import solve24


class NiceGUIAPP:
    result_text: str
    numbers: list[ui.select]
    result_statement: ui.markdown
    result_list: ui.list

    def __init__(self) -> None:
        self.result_text = ""

        self.title = "Make 24"
        self.favicon = Path("favicon.ico")
        self.build_ui()

    def build_ui(self):
        @ui.page(path="/")
        def ui_body():
            # A container with space to both sides
            with ui.grid(columns=12).classes("w-full gap-0"):
                ui.space().classes("col-span-1")
                container = ui.column().classes("col-span-10 items-center")
                ui.space().classes("col-span-1")

            with container:
                with ui.row().classes("w-full justify-center bg-primary"):
                    ui.label("Make 24").classes().style("font-size: 200%")

                # NOTE dark mode will be persistent for each user across tabs and server restarts
                ui.dark_mode().bind_value(app.storage.user, "dark_mode")
                ui.checkbox("dark mode").bind_value(app.storage.user, "dark_mode")

                with ui.row():
                    self.numbers = [
                        ui.select(list(range(1, 14)), value=(i + 1) * 2)
                        for i in range(4)
                    ]

                ui.button("GO!", on_click=self.calc_24_result)

                self.result_statement = ui.markdown().bind_content_from(
                    self, "result_text"
                )
                self.result_list = ui.list().props("dense separator")

    def run(self):
        ui.run(
            title=self.title,
            favicon=self.favicon,
            storage_secret="pick your private secret here",  # NOTE setting a secret is optional but allows for persistent storage per user
        )

    def run_with_fastapi(self, fastapi_app: FastAPI):
        ui.run_with(
            fastapi_app,
            title=self.title,
            favicon=self.favicon,
            # mount_path='/gui',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
            storage_secret="pick your private secret here",  # NOTE setting a secret is optional but allows for persistent storage per user
        )

    def calc_24_result(self):
        nums = [int(self.numbers[i].value) for i in range(4)]
        all_result_24 = solve24(*nums)

        self.result_text = f"With number(s) {nums}, "
        self.result_text += f"there is/are {len(all_result_24)} solution(s) in total:\n"

        self.result_list.clear()
        with self.result_list:
            for item in all_result_24:
                ui.item(str(item))


if __name__ in {"__main__", "__mp_main__"}:
    NiceGUIAPP().run()
