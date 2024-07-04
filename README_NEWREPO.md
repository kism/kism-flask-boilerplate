# mycoolapp

## Run

### Run Dev

```bash
poetry install
poetry shell
flask --app mycoolapp run --port 5000
```

### Run Prod

```bash
poetry install --only main
.venv/bin/waitress-serve \
    --listen "127.0.0.1:5000" \
    --trusted-proxy '*' \
    --trusted-proxy-headers 'x-forwarded-for x-forwarded-proto x-forwarded-port' \
    --log-untrusted-proxy-headers \
    --clear-untrusted-proxy-headers \
    --threads 4 \
    --call mycoolapp:create_app
```

## Settings

### Flask Settings

`instance/flask.toml`

for example:

```toml
    DEBUG = true
```

### App Settings

Defaults are defined in mycoolapp_settings.py, and settings loading and validation are handled in there too.