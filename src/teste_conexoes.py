"""Testa as conexoes com Supabase (Postgres) e Redis.

Uso (dentro de src/):  python teste_conexoes.py
Le as variaveis do arquivo .env.
"""
import os

import psycopg2
import redis
from dotenv import load_dotenv

load_dotenv()


def testar_supabase():
    url = os.environ.get('DATABASE_URL', '')
    if not url or 'SUA_SENHA' in url:
        print('[Supabase] DATABASE_URL nao preenchida no .env')
        return
    try:
        with psycopg2.connect(url, connect_timeout=15, sslmode='require') as con:
            with con.cursor() as cur:
                cur.execute('SELECT current_database(), current_user')
                banco, usuario = cur.fetchone()
        print(f'[Supabase] OK - banco={banco} usuario={usuario}')
    except Exception as erro:
        print(f'[Supabase] FALHA - {type(erro).__name__}: {erro}')


def testar_redis():
    url = os.environ.get('REDIS_URL', '')
    if not url or 'SUA_SENHA' in url:
        print('[Redis] REDIS_URL nao preenchida no .env')
        return
    try:
        r = redis.from_url(url, socket_connect_timeout=5)
        r.ping()
        print('[Redis] OK - PING respondeu')
    except Exception as erro:
        print(f'[Redis] FALHA - {type(erro).__name__}: {erro}')


if __name__ == '__main__':
    testar_supabase()
    testar_redis()
