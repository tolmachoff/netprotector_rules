import flet as ft

from controller import Controller
import rule_parser


def main(page: ft.Page):
    page.title = "Netprotector rules"
    page.window_maximized = True

    controller = Controller()

    rules_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Message")),
            ft.DataColumn(ft.Text("Protocol")),
        ],
    )

    rule_text = ft.Column(
        [
            ft.Text("Rule text:"),
            ft.TextField(
                read_only=True,
                multiline=True,
            )
        ]
    )

    def create_rule_clicked_callback(n):
        def clbk(_):
            if controller.select(n):
                # First click - print rule text
                rule_text.controls[1].value = controller.get_rule(n)
                rule_text.update()
            else:
                # Not first click - toggle rule select
                rules_data_table.rows[n].selected = controller.get_is_selected(n)
                rules_data_table.update()

        return clbk

    def update_rules_data_table():
        rules_data_table.rows.clear()
        for cnt, rule in enumerate(controller.get_rules()):
            msg = rule_parser.get_message(rule)
            protocol = rule_parser.get_protocol(rule)
            rules_data_table.rows.append(
                ft.DataRow(
                    [
                        ft.DataCell(ft.Text(msg)),
                        ft.DataCell(ft.Text(protocol)),
                    ],
                    on_select_changed=create_rule_clicked_callback(cnt),
                )
            )
        rules_data_table.update()

    def open_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            controller.load_rules(e.files[0].path)
            update_rules_data_table()

    open_file_dialog = ft.FilePicker(on_result=open_file_result)
    page.overlay.append(open_file_dialog)

    def do_open(_):
        open_file_dialog.pick_files(dialog_title="Open rules file")

    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            controller.export_rules(e.path)

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(save_file_dialog)

    def do_export(_):
        save_file_dialog.save_file(
            dialog_title="Save encripted rules file",
            file_name="result.base64"
        )

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
                        rules_data_table,
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                ),

                ft.Column(
                    [
                        rule_text,
                    ],
                    expand=True,
                )
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),

        ft.Row(
            [
                ft.ElevatedButton("Select all"),
                ft.TextField(label="Filter"),
            ]
        ),

    )

    page.update()


ft.app(target=main)
