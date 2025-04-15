#!/bin/sh

echo "⏳ Ждем, пока PostgreSQL будет готов..."
/wait-for-it.sh db:5432 --timeout=60 --strict -- echo "✅ PostgreSQL готов"

echo "⏳ Ждем, пока Redis будет готов..."
/wait-for-it.sh redis:6379 --timeout=60 --strict -- echo "✅ Redis готов"

echo "⚙️ Запускаем миграции Alembic..."
alembic upgrade head

echo "✅ Добавляем начальные данные..."
python data_generate.py

echo "🚀 Запускаем Flask..."
exec python main.py
