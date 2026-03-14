# **PostgreSQL Core**

*An educational project showcasing how to use PostgreSQL with Python, covering both synchronous and asynchronous approaches.*

> ⚠️ **This repository is archived.**  
While the server setup and configuration remain unchanged, the Python code (SQLAlchemy patterns, repositories, services) is periodically revised as better approaches are discovered or past decisions are reconsidered. Maintaining identical changes across three separate repositories has no practical value, so active development continues only in [sqlite-core](https://github.com/Sierra-Arn/sqlite-core). Refer to that project for the latest Python implementation.

## **Project Structure**

```bash
postgresql-core/
├── app/                   # Main application code
├── docker-composes/       # Docker Compose configurations for PostgreSQL servers
├── .env.example           # Example environment variables file
├── justfile               # Project-specific commands using Just
├── pixi.lock              # Locked dependency versions for reproducible environments
├── pixi.toml              # Pixi project configuration: environments, dependencies, and platforms
└── playground-testing/    # Jupyter notebooks for playground testing
```

Each directory includes its own `README.md` with detailed information about its contents and usage, and every file contains comprehensive inline comments to explain the code.

## **Dependencies Overview**

- [pydantic-settings](https://github.com/pydantic/pydantic-settings) — 
a Pydantic-powered library for managing application configuration and environment variables with strong typing, validation, and seamless `.env` support.

- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) — 
the Python SQL toolkit and Object-Relational Mapper (ORM) used as the foundation for database modeling, querying, and transaction management in both synchronous and asynchronous contexts.

- [Alembic](https://github.com/sqlalchemy/alembic) — 
a lightweight database migration tool for SQLAlchemy, enabling structured, version-controlled evolution of the PostgreSQL schema over time.

- [psycopg2-binary](https://github.com/psycopg/psycopg2) — 
the most popular Python client for PostgreSQL, enabling synchronous database connections and operations.

- [asyncpg](https://github.com/MagicStack/asyncpg) — 
a fast Python client for PostgreSQL, enabling asynchronous database connections and operations.

- [just](https://github.com/casey/just) — 
a lightweight, cross-platform command runner that replaces complex shell scripts with clean, readable, and reusable project-specific recipes. [^1]

[^1]: Despite using `pixi`, there are issues with `pixi tasks` regarding environment variable handling from `.env` files and caching mechanism that is unclear and causes numerous errors. In contrast, `just` provides predictable, transparent execution without the complications encountered with `pixi tasks` system. I truly hope `pixi tasks` have been improved by the time you’re reading this! <33

### **Testing & Development Dependencies**

- [JupyterLab](https://github.com/jupyterlab/jupyterlab) — 
a next-generation web-based interactive development environment for Jupyter notebooks; used here to create interactive documents for testing and verifying code execution.

## **Quick Start**

### **I. Prerequisites**

- [Docker and Docker Compose](https://docs.docker.com/engine/install/).
- [Pixi](https://pixi.sh/latest/) package manager.

> **Platform note**: All development and testing were performed on `linux-64`.  
> If you're using a different platform, you’ll need to:
> 1. Update the `platforms` list in the `pixi.toml` accordingly.
> 2. Ensure that platform-specific scripts are compatible with your operating system or replace them with equivalents.

### **II. Database Setup**

1. **Clone the repository**

    ```bash
    git clone git@github.com:Sierra-Arn/postgresql-core.git
    cd postgresql-core
    ```

2. **Install dependencies**
    
    ```bash
    pixi install --all
    ```

3. **Activate pixi environment**
    
    ```bash
    pixi shell
    ```

4. **Setup environment configuration**
   ```bash
   just copy-env
   just make-x
   ```

5. **Start PostgreSQL database**
   ```bash
   just postgres-up 2
   ```

6. **Create a database migration & Apply it**
   ```bash
   just alembic-revision
   just alembic-upgrade
   ```

### **III. Testing**

Once a database is ready, you can run and test the PostgreSQL implementation with interactive Jupyter notebooks in `playground-testing/`:

1. **Launch JupyterLab**

    ```bash
    pixi run -e test jupyter lab
    ```

2. **Test the PostgreSQL implementation**
    - JupyterLab should open automatically in your browser at the default address.
    - In JupyterLab, navigate to the `playground-testing/` folder.
    - Open and execute the notebooks interactively.

3. **(Optional) Verify database manually**  
You can open a PostgreSQL shell to manually verify that everything is working correctly:

    ```bash
    just postgres-shell 2
    ```

### **IV. Cleanup**

When you finish testing:

1. **Stop JupyterLab**  
   In the terminal where JupyterLab is running, press `Ctrl+C` to shut it down.

2. **Stop PostgreSQL**

    ```bash
    just postgres-down 2
    ```

## **License**

This project is licensed under the [BSD-3-Clause License](LICENSE).