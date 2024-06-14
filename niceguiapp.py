from pathlib import Path

from fastapi import FastAPI
from nicegui import app, ui

from make24_solver import solve24


title = "Make 24"
favicon = Path("favicon.ico")


@ui.page(path="/")
def ui_body():
    def calc_24_result():
        nums = [int(numbers[i].value) for i in range(4)]
        all_result_24 = solve24(*nums)

        result_statement.content = f"With number(s) {nums}, there is/are {len(all_result_24)} solution(s) in total:\n"

        result_list.clear()
        with result_list:
            for item in all_result_24:
                ui.item(str(item))

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
            numbers = [
                ui.select(list(range(1, 14)), value=(i + 1) * 2) for i in range(4)
            ]

        ui.button("GO!", on_click=calc_24_result)

        result_statement = ui.markdown()
        result_list = ui.list().props("dense separator")


def run_with_fastapi(fastapi_app: FastAPI):
    ui.run_with(
        fastapi_app,
        title=title,
        favicon=favicon,
        # mount_path='/gui',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret="pick your private secret here",  # NOTE setting a secret is optional but allows for persistent storage per user
    )


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title=title,
        favicon=favicon,
        storage_secret="pick your private secret here",  # NOTE setting a secret is optional but allows for persistent storage per user
    )
