class PluginRegistry:
    def __init__(self):
        self.plugins = []

    def register(self, plugin):
        self.plugins.append(plugin)

    def get_plugins_for_intent(self, intent):
        return [p for p in self.plugins if p.can_handle(intent)]

registry = PluginRegistry()
