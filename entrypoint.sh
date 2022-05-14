#!/bin/sh

# Initalizing the DB
if $INITIALIZE_DB = true; then
    echo "Initalizing Database"
    aerich init -t api.core.tortoise_config.tortoise_config
    aerich init-db
fi

# Migrating the DB
if $MIGRATE_DB = true; then
    echo "Migrating Database"
    aerich migrate
    aerich upgrade
fi

uvicorn api.__main__:app --host 0.0.0.0 --reload