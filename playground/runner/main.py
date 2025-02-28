from apexdevkit.server import UvicornServer

from playground.core.services.classes.repositroy_sql_lite_chooser import SqlLiteChooser
from playground.runner.setup import SetupConfiguration, setup

if __name__ == "__main__":
    UvicornServer.from_env().run(setup(SetupConfiguration(repository_chooser=SqlLiteChooser())))
