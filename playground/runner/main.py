from apexdevkit.server import UvicornServer

from playground.runner.setup import SetupConfiguration, setup

if __name__ == "__main__":
    UvicornServer.from_env().run(setup(SetupConfiguration.for_production()))
