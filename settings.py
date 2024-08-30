import os

import pydash
import toml

_script_dir = os.path.dirname(__file__)

config_path = os.path.join(_script_dir, "config.toml")

assert os.path.exists(
    config_path
), "config.toml not found. Use make config to create one."

config = toml.load(config_path)

assert config, "config.toml is empty, please fill it with the necessary data"

ENV = "test" if pydash.get(config, "debug", True) else "prod"


class MySqlConfig:
    HOST = pydash.get(config, f"db.{ENV}.host")
    PORT = pydash.get(config, f"db.{ENV}.port")
    USER = pydash.get(config, f"db.{ENV}.username")
    PASSWORD = pydash.get(config, f"db.{ENV}.password")
    DATABASE = pydash.get(config, f"db.{ENV}.database")


assert MySqlConfig.HOST, "Database host not found in config.toml"
assert MySqlConfig.PORT, "Database port not found in config.toml"
assert MySqlConfig.USER, "Database user not found in config.toml"
assert MySqlConfig.PASSWORD, "Database password not found in config.toml"
assert MySqlConfig.DATABASE, "Database name not found in config.toml"
