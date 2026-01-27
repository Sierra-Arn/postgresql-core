# app/db/config.py
from urllib.parse import quote_plus
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSQLConfig(BaseSettings):
    """
    Configuration schema for PostgreSQL database.

    Attributes
    ----------
    host : str
        Hostname or IP address of the PostgreSQL server. Default is `"127.0.0.1"`.
    external_port : int
        TCP port the server listens on. Must be in the range 1-65535.
        Default is `5432` (standard PostgreSQL port).
    username : str
        Database user name.
    password : str
        Database user password.
    db_name : str
        Name of the PostgreSQL database to connect to.
    echo : bool, optional
        Enables or disables SQL statement logging to stdout.
        Useful for debugging during development; should be `False` in production.
        Default is `False`.
    autocommit : bool, optional
        Controls whether SQLAlchemy sessions automatically commit transactions.
        When `False` (recommended), explicit `commit()` calls are required.
        Default is `False`.
    autoflush : bool, optional
        Controls whether pending ORM changes are automatically flushed before queries.
        When `False` (recommended), flushing is manual, giving full control over side effects.
        Default is `False`.
    expire_on_commit : bool, optional
        Determines whether ORM objects are expired (i.e., their attributes detached from the session)
        immediately after a transaction is committed.
        
        When `True` (SQLAlchemy's default), all loaded attributes of ORM instances are marked as "expired"
        upon `session.commit()`. Any subsequent access to these attributes triggers an implicit
        database refresh (lazy load) to ensure data consistency. While safe in synchronous contexts,
        this behavior is **incompatible with asynchronous applications** when serializing ORM objects
        after commit: Pydantic's `model_validate()` is a purely synchronous function and cannot
        perform the required `await`-based I/O to reload expired attributes. This results in a
        `MissingGreenlet` error during attribute access.
        
        Therefore, in async applications, this setting **must be `False`** to preserve attribute values post-commit and 
        allow safe serialization of ORM objects into Pydantic response models.
        
        Default is `False`.
         
    Notes:
    ------
    1. Automatically loads settings from a `.env` file in the current working directory
       using a module-specific prefix specified.
    2. The `.env` file must use UTF-8 encoding. 
    3. Variable names are case-insensitive.
    4. Any extra (unrecognized) variables are silently ignored.
    5. The configuration is immutable after instantiation.
    6. During instantiation, values are resolved in the following order of precedence 
       (from highest to lowest priority):
        1. **Explicitly passed arguments** — values provided directly to the constructor.
        2. **Environment variables** — including those loaded from the `.env` file,
           prefixed according to the subclass's `env_prefix`.
        3. **Code-defined defaults** — fallback values specified as field defaults
           in the class definition.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        frozen=True,
        env_prefix="POSTGRESQL_"
    )

    host: str = "127.0.0.1"
    external_port: int = Field(default=5432, ge=1, le=65535)
    username: str
    password: str
    db_name: str
    echo: bool = False
    autocommit: bool = False
    autoflush: bool = False
    expire_on_commit: bool = False

    @property
    def sync_database_url(self) -> str:
        """
        Build synchronous PostgreSQL database connection URL from configuration settings.

        Returns
        -------
        str
            Complete PostgreSQL connection URL with credentials in the format:
            postgresql+psycopg2://username:password@host:port/db_name
        
        Notes
        -----
        The password is URL-encoded using `quote_plus` to safely handle
        special characters that might be present in the password string.
        """

        return (
            f"postgresql+psycopg2://{self.username}:{quote_plus(self.password)}"
            f"@{self.host}:{self.external_port}/{self.db_name}"
        )
    
    @property
    def async_database_url(self) -> str:
        """
        Build asynchronous PostgreSQL database connection URL from configuration settings.

        Returns
        -------
        str
            Complete PostgreSQL connection URL with credentials in the format:
            postgresql+asyncpg://username:password@host:port/db_name
        
        Notes
        -----
        The password is URL-encoded using `quote_plus` to safely handle
        special characters that might be present in the password string.
        """

        return (
            f"postgresql+asyncpg://{self.username}:{quote_plus(self.password)}"
            f"@{self.host}:{self.external_port}/{self.db_name}"
        )


# Initialize PostgreSQL configuration singleton
# Since PostgreSQL database settings are static for the application's lifetime
# and any configuration changes require a full application restart,
# it is safe to instantiate the config once at module level and reuse
# it throughout the application as a singleton.
postgres_config = PostgreSQLConfig()