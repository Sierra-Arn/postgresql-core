# **Docker Compose Configurations**

This README gives a concise overview of the Docker Compose configurations: what each file is for and when to use it. For detailed configuration notes, environment variables, and usage commands are in `.env.example` and the `justfile`.

## **Files**

To keep configuration **readable and incremental**, the setup is split into three progressively layered files. Each adds only new directives — and comments **only the additions**, assuming familiarity with the previous stage.

1. **`docker-compose.1-init.yml`**  
Base PostgreSQL container: minimal config with essential settings and inline explanations.

2. **`docker-compose.2-shell.yml`**  
Builds on (1) — adds interactive shell access. Only new lines are commented.

3. **`docker-compose.3-persistent.yml`**  
Builds on (2) — adds persistent volumes. Again, comments cover only what’s new.