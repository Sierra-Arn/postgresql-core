# **Testing and Exploration**

Two Jupyter notebooks are provided for interactive experimentation with PostgreSQL: one for synchronous workflows, another for asynchronous ones.

Additionally, you can always connect directly to the PostgreSQL container and manually inspect the database state using standard psql commands like:

1. **View all databases:**
    ```sql
    \l
    ```

2. **View all users/roles:**
    ```sql
    \du
    ```

3. **View all tables in current database:**
    ```sql
    \dt
    ```

4. **View structure of specific table:**
    ```sql
    \d <table_name>
    ```

5. **View all schemas:**
    ```sql
    \dn
    ```

6. **View data in table:**
    ```sql
    SELECT * FROM <table_name>;
    ```

7. **Exit psql:**
    ```sql
    \q
    ```