from configparser import ConfigParser
import psycopg2

# todo: make error handeling better if file does not exist


def load_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return config


if __name__ == "__main__":
    config = load_config()
    print(config)
    try:
        params = config
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Connected to database. Database version: {db_version}")
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
