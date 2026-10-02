# A.S.A.S Core

High-performance payment infrastructure with idempotent transactions, Redis Streams, and production-ready architecture.

## Features

- ✅ Idempotent transactions (no double-spending)
- ✅ Redis Streams for durable queuing
- ✅ Row-level locking (with_for_update)
- ✅ Full audit logging
- ✅ JWT authentication + refresh tokens
- ✅ Rate limiting (1000 req/min)
- ✅ PostgreSQL with timezone-aware timestamps
- ✅ Decimal-safe (integer cents, no float)
- ✅ Prometheus metrics
- ✅ Kubernetes-ready

## Quick Start

```bash
git clone [https://github.com/yourusername/paystream.git](https://github.com/yourusername/paystream.git)
cd paystream
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set SECRET_KEY
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
