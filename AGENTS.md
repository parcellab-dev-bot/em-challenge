# Repository

## Structure

- `returns_portal/`: Django project configuration
- `portal/`: application code
- `portal/services/`: mapping and eligibility logic
- `portal/templates/returns/`: Django and HTMX templates
- `portal/data/`: sample orders and rules configuration
- `portal/tests/`: test suite
- `manage.py`: Django command entrypoint

## Commands

```bash
uv sync
uv run pytest
uv run python manage.py runserver
```
