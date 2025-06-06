import configparser
import os

import psycopg2


def get_db_config(path=None):
    config = configparser.ConfigParser()

    if not path:
        path = os.path.join(os.path.dirname(__file__), "..", "config", "database.ini")
    config.read(path)
    return config["postgresql"]


def create_connection():
    cfg = get_db_config()
    try:
        return psycopg2.connect(
            host=cfg["server"],
            database=cfg["database"],
            user=cfg["user"],
            password=cfg["password"],
            port=cfg["port"]
        )
    except Exception as e:
        print("Error, couldn't connect to database.", e)
        raise

