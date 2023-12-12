import flet as ft

from controller import Controller
from rule_text import RuleText
from rules_data_table import RulesDataTable


def main(page: ft.Page):
    page.title = "Netprotector rules"
    page.window_maximized = True

    controller = Controller()
    rule_text = RuleText()
    rules_data_table = RulesDataTable(controller, rule_text)

    def open_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            controller.load_rules(e.files[0].path)
            rules_data_table.update()

    open_file_dialog = ft.FilePicker(on_result=open_file_result)

    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            controller.export_rules(e.path)

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    
    page.overlay.extend(
        [
            open_file_dialog,
            save_file_dialog
        ]
    )

    def do_open(e):
        open_file_dialog.pick_files(dialog_title="Open rules file")

    def do_export(e):
        save_file_dialog.save_file(
            dialog_title="Save encripted rules file",
            file_name="result.base64"
        )

    def do_select_all(e):
        controller.toggle_select_filtered()
        rules_data_table.update()

    def do_apply_filter(e):
        controller.apply_filter(e.control.value)
        rules_data_table.update()

    page.add(
        ft.Row(
            [
                ft.ElevatedButton("Open", on_click=do_open),
                ft.ElevatedButton("Export", on_click=do_export),
            ],
        ),

        ft.Row(
            [
                ft.Column(
                    [
                        rules_data_table.view,
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                ),

                ft.Column(
                    [
                        rule_text.view,
                    ],
                    expand=True,
                )
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),

        ft.Row(
            [
                ft.ElevatedButton("Select all", on_click=do_select_all),
                ft.TextField(label="Filter", on_submit=do_apply_filter),
            ]
        ),

    )

    page.update()


ft.app(target=main)
