from apexdevkit.server import UvicornServer

from playground.runner.setup import setup, SetupConfiguration, MemoryType

if __name__ == "__main__":
    UvicornServer.from_env().run(setup(SetupConfiguration(MemoryType.IN_MEMORY)))
