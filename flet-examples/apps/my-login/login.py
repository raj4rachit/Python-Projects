import flet as ft

def main(page: ft.Page):
    page.add(ft.Text(value="Hello, world!"))
    page.horizontal_alignment = "center"
    page.vertical_alignment = "spaceBetween"

    top = ft.Text(f"Top: {page.window_top}")
    left = ft.Text(f"Left: {page.window_left}")
    display_width = ft.Text(f"Width: {page.width}")
    display_height = ft.Text(f"Height: {page.height}")
    page.window_resizable = False
    page.window_width = 1000
    page.window_height = 700
    page.update()

ft.app(target=main)