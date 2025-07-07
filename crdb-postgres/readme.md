# Data migrate from CockroachDB to PostgreSQL via FDW

Foreign Data Wrappers - https://wiki.postgresql.org/wiki/Foreign_data_wrappers

### Step by step migration

1. Create server and user mapping

```sql
CREATE SERVER crdb_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (dbname 'postgres', host '0.0.0.0', port '26000');
```

```sql
CREATE USER MAPPING FOR root
SERVER crdb_server
OPTIONS (USER 'root'); -- without password
```

2. Allow the user to work with FDW

```sql
GRANT ALL ON DATABASE test TO root;
GRANT USAGE ON FOREIGN SERVER crdb_server TO root;
```

3. Import schema and test remote connect
```sql
IMPORT FOREIGN SCHEMA public LIMIT TO (test)
FROM SERVER crdb_server INTO public;
```

```sql
SELECT * FROM test; -- remote select
-- data from cockroachdb
```

4. Copy remote table to the local

```sql
CREATE TABLE local_test (LIKE test INCLUDING ALL);
```

```sql
INSERT INTO local_test SELECT * FROM test;
```

```sql
SELECT * FROM local_test; -- remote select
-- data from cockroachdb on local postgres
```