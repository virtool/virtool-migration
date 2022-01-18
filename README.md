# virtool-migration

Migrations for Virtool's PostgreSQL database written using Alembic.

## Usage

Run the latest migration Docker image in your stack.

The `SQLALCHEMY_URL` environment variable must be set:

_Command Line_
```shell
docker run -e SQLALCHEMY_URL="postgresql://virtool:virtool@localhost/virtool" virtool/migration:1.1.2 
```

_Kubernetes_
```yaml
spec:
  containers:
    - name: migration
      image: virtool/migration:1.1.2
      env:
        - name: SQLALCHEMY_URL
          value: "postgresql://virtool:virtool@localhost/virtool"
```

The following command is executed on container start:
```shell
alembic upgrade head
```

This will bring your database up-to-date with the most recent change.

You can override the command to target a different revision:

_Command Line_
```shell
docker run virtool/migration:1.1.2 alembic upgrade 90bf491700cb

```

_Kubernetes_
```yaml
spec:
  containers:
    - name: migration
      image: virtool/migration:1.1.2
      command: "alembic upgrade 90bf491700cb"
      env:
        - name: SQLALCHEMY_URL
          value: "postgresql://virtool:virtool@localhost/virtool"
```


## Known Issues

If migrations are applied while a transaction is open in `asyncpg` in another service, it will fail due to the change in
schema.

We are still working on a solution for this.
