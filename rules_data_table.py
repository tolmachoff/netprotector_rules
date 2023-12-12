import flet as ft
import rule_parser


class RulesDataTable:

    def __init__(self, controller, rule_text):
        self.view = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Message")),
                ft.DataColumn(ft.Text("Protocol")),
            ],
        )

        self._rule_text = rule_text
        self._controller = controller

        self._last_clicked = -1

    def update(self):
        def create_callback(i):
            def clbk(e):
                real_i = self._controller.get_filtered_indexes()[i]
                if self._last_clicked != real_i:
                    self._last_clicked = real_i
                    self._rule_text.set_value(self._controller.get_rules()[real_i])
                else:
                    self.view.rows[i].selected = self._controller.toggle_select(real_i)
                    self.view.update()
            return clbk
        
        self._last_clicked = -1
        self.view.rows.clear()
        for i, rule in enumerate(self._controller.get_filtered_rules()):
            real_i = self._controller.get_filtered_indexes()[i]
            msg = rule_parser.get_message(rule)
            protocol = rule_parser.get_protocol(rule)
            self.view.rows.append(
                ft.DataRow(
                    [
                        ft.DataCell(ft.Text(msg)),
                        ft.DataCell(ft.Text(protocol)),
                    ],
                    selected=self._controller.get_is_selected(real_i),
                    on_select_changed=create_callback(i),
                )
            )
        self.view.update()
