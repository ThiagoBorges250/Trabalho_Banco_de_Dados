"""Cliente da API do Supabase (opcional).

O sistema usa o Postgres do Supabase via Django ORM (DATABASE_URL). Este
cliente so e necessario se voce quiser usar Storage, Auth ou a API REST.
"""
from functools import lru_cache

from django.conf import settings


@lru_cache(maxsize=1)
def get_supabase():
    from supabase import create_client

    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise RuntimeError('Defina SUPABASE_URL e SUPABASE_KEY no .env')
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
