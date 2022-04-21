from api.config import db_config

tortoise_config = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": db_config.db,
                "host": db_config.host,
                "password": db_config.password,
                "port": db_config.port,
                "user": db_config.user,
            },
        }
    },
    "apps": {
        "main": {
            "models": [
                "api.core.books.models",
                "aerich.models",
                "api.core.borrowed.models",
                "api.core.returned.models",
                "api.core.students.models",
                "api.core.auth.models",
            ],
            "default_connection": "default",
        }
    },
}
