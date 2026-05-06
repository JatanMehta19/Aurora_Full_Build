class AuroraRuntimeError(Exception):
    def __init__(self, msg, line=None):
        prefix = f"[Line {line}] " if line else ""
        super().__init__(f"{prefix}Runtime Error: {msg}")

class Environment:
    def __init__(self, parent=None):
        self.vars = {}  # name -> {value, mutable}
        self.parent = parent

    def define(self, name, value, mutable=True):
        self.vars[name] = {"value": value, "mutable": mutable}

    def get(self, name):
        if name in self.vars: return self.vars[name]["value"]
        if self.parent: return self.parent.get(name)
        raise AuroraRuntimeError(f"Undefined variable '{name}'")

    def assign(self, name, value):
        if name in self.vars:
            if not self.vars[name]["mutable"]:
                raise AuroraRuntimeError(f"Cannot reassign immutable variable '{name}'")
            self.vars[name]["value"] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise AuroraRuntimeError(f"Undefined variable '{name}'")