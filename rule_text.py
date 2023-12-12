import flet as ft


class RuleText:

    def __init__(self):
        self.view = ft.Column(
            [
                ft.Text("Rule text:"),
                ft.TextField(
                    read_only=True,
                    multiline=True,
                )
            ]
        )
    
    def set_value(self, val):
        self.view.controls[1].value = val
        self.view.update()
