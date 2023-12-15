from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Modify the path accordingly to your project structure
import sys
from pathlib import Path

# Add the path to the directory containing your models
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))

from database import Base  # Import your SQLAlchemy Base class

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Add your models to the target_metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")

# ... more imports and configurations may be necessary based on your project structure

# override for context.configure() to work
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

# override for context.configure() to work
def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# main() function called when run_migrations_online() is called
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
