# Autoghost

Automated backend system for running faceless TikTok/YouTube accounts.

## Setup

```bash
python3 -m venv runauto
source runauto/bin/activate
pip install -r requirements.txt
cp .env.sample .env
```

Edit `.env` with your database path, then initialize:

```bash
mkdir data
python -c "from core.database import init_db; init_db()"
```

## Verify

```bash
python -c "from configs.config import DATABASE_PATH; print(DATABASE_PATH)"
python -c "from core.database import init_db; init_db()"
```
