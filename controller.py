import base64_encoder


class Controller:
    def __init__(self):
        self._rules = []
        self._selected = set()
        self._current = -1
        self._was_select_multiple = False

    def load_rules(self, filepath):
        self._rules.clear()
        self._selected.clear()
        self._current = -1
        with open(filepath) as f:
            for line in f:
                self._rules.append(line.rstrip())

    def get_rules(self):
        return self._rules

    def get_rule(self, n):
        return self._rules[n]
        
    def set_is_selected(self, n, val):
        if val:
            self._selected.add(n)
        else:
            self._selected.remove(n)

    def get_is_selected(self, n):
        return n in self._selected
    
    def select(self, n):
        if self._current != n:
            self._current = n
            return True
        else:
            self.set_is_selected(n, not self.get_is_selected(n))
            return False

    def select_multiple(self):
        if not self._was_select_multiple:
            self._was_select_multiple = True
            
        else:
            self._was_select_multiple = False

    def export_rules(self, filepath):
        rules_to_save = ""
        selected = list(self._selected)
        selected.sort()
        for i in selected:
            rules_to_save += self._rules[i] + "\n"
        encoded_rules_to_save = base64_encoder.encode(rules_to_save)
        with open(filepath, "w") as f:
            f.write(encoded_rules_to_save)
