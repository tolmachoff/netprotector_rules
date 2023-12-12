import base64_encoder


class Controller:

    def __init__(self):
        self._rules = []

        self._filtered_indexes = []
        self._filtered_rules = []
        self._filter = ""

        self._selected = set()

        self._was_toggle_select_all = False

    def _update_filtered_rules(self):
        self._filtered_indexes.clear()
        self._filtered_rules.clear()

        for cnt, rule in enumerate(self._rules):
            if rule.lower().count(self._filter.lower()) > 0:
                self._filtered_indexes.append(cnt)
                self._filtered_rules.append(rule)

    def load_rules(self, filepath):
        self._rules.clear()
        self._selected.clear()
        self._was_toggle_select_all = False

        with open(filepath) as f:
            for line in f:
                self._rules.append(line.rstrip())
        
        self._update_filtered_rules()

    def export_rules(self, filepath):
        rules_to_save = ""
        selected = list(self._selected)
        selected.sort()
        for i in selected:
            rules_to_save += self._rules[i] + "\n"
        encoded_rules_to_save = base64_encoder.encode(rules_to_save)
        with open(filepath, "w") as f:
            f.write(encoded_rules_to_save)

    def apply_filter(self, filter: str):
        self._was_toggle_select_all = False

        self._filter = filter
        self._update_filtered_rules()

    def get_rules(self) -> list:
        return self._rules
    
    def get_filtered_indexes(self) -> list:
        return self._filtered_indexes

    def get_filtered_rules(self) -> list:
        return self._filtered_rules

    def get_is_selected(self, n) -> bool:
        return n in self._selected

    def set_is_selected(self, n, val):
        if val:
            self._selected.add(n)
        else:
            self._selected.remove(n)

    def toggle_select(self, n) -> bool:
        res = not self.get_is_selected(n)
        self.set_is_selected(n, res)
        return res

    def toggle_select_filtered(self):
        new_state = not self._was_toggle_select_all
        for i in self._filtered_indexes:
            self.set_is_selected(i, new_state)
        self._was_toggle_select_all = new_state
