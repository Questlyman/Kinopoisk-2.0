## Migration models

From root directory of project

Auto-generating migration script and updating models:

```bash
alembic revision --autogenerate -m "message"
alembic upgrade head
```

Downgrade of models:

```bash
alembic downgrade <target-revision>
```