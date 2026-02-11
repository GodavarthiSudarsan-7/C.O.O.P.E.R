from cooper.shell import run_shell
from cooper.work.plugin_registry import registry
from cooper.work.planner_plugin import PlannerPlugin
from cooper.work.executor_plugin import ExecutorPlugin
from cooper.work.critic_plugin import CriticPlugin
from cooper.work.responder_plugin import ResponderPlugin

def main():
    registry.register(PlannerPlugin())
    registry.register(CriticPlugin())
    registry.register(ExecutorPlugin())
    registry.register(ResponderPlugin())
    run_shell()

if __name__ == "__main__":
    main()
