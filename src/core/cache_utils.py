"""Cache com Redis para as consultas mais pesadas do sistema.

PROBLEMA: o banco (Supabase) fica na internet. Telas como o Dashboard
(7 consultas COUNT), o Relatorio da View (4 JOINs) e a Media do aluno
(Function) repetem as mesmas consultas a cada acesso, e cada ida ao banco
custa centenas de milissegundos.

SOLUCAO: a primeira consulta vai ao Supabase e o resultado e guardado no
Redis (memoria, resposta em poucos ms). As proximas leituras vem do Redis.

CONSISTENCIA: toda gravacao (cadastro, edicao, exclusao, procedure) chama
invalidar(), que incrementa uma "versao dos dados". As chaves antigas deixam
de ser usadas, entao a tela nunca mostra dado desatualizado.

Se o Redis cair, o sistema continua funcionando: consulta direto o banco.
"""
import time

from django.core.cache import cache

TTL_PADRAO = 300  # segundos (5 minutos)
CHAVE_VERSAO = 'dados_versao'
CHAVE_HITS = 'stat_hits'
CHAVE_MISSES = 'stat_misses'
PREFIXO = 'dados'

_AUSENTE = object()


def _incrementar(chave):
    try:
        cache.incr(chave)
    except ValueError:
        cache.set(chave, 1, None)


def versao():
    """Versao atual dos dados (faz parte do nome de todas as chaves)."""
    v = cache.get(CHAVE_VERSAO)
    if v is None:
        cache.add(CHAVE_VERSAO, 1, None)
        v = cache.get(CHAVE_VERSAO) or 1
    return v


def invalidar():
    """Chamada sempre que os dados mudam no banco."""
    try:
        _incrementar(CHAVE_VERSAO)
    except Exception:
        pass  # Redis fora do ar: nada a invalidar


def obter(nome, calcular, ttl=TTL_PADRAO):
    """Retorna (valor, info). `calcular` e uma funcao sem argumentos que
    faz a consulta no banco; so e chamada quando o Redis nao tem o dado."""
    inicio = time.perf_counter()
    redis_ok = True
    chave = f'{PREFIXO}:{nome}'
    valor = _AUSENTE

    try:
        chave = f'{PREFIXO}:{nome}:v{versao()}'
        valor = cache.get(chave, _AUSENTE)
    except Exception:
        redis_ok = False

    if valor is not _AUSENTE:
        try:
            _incrementar(CHAVE_HITS)
        except Exception:
            pass
        origem = 'redis'
    else:
        valor = calcular()
        origem = 'supabase'
        if redis_ok:
            try:
                cache.set(chave, valor, ttl)
                _incrementar(CHAVE_MISSES)
            except Exception:
                redis_ok = False

    info = {
        'origem': origem,
        'ms': round((time.perf_counter() - inicio) * 1000, 1),
        'chave': chave,
        'ttl': ttl,
        'redis_ok': redis_ok,
    }
    return valor, info


def estatisticas():
    try:
        return {
            'hits': cache.get(CHAVE_HITS, 0),
            'misses': cache.get(CHAVE_MISSES, 0),
            'versao': versao(),
        }
    except Exception:
        return {'hits': 0, 'misses': 0, 'versao': '-'}
