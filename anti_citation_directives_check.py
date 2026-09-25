#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anti-citation-directives-check — varre um HTML atrás de diretivas que
bloqueiam citação e snippet, e que às vezes acabam na página sem o dono
perceber (herdadas de template, plugin de SEO mal configurado, ou copiadas
de outro projeto).

O QUE FAZ
    Procura, no HTML:

    1. `<meta name="robots">` (ou `googlebot`, `bingbot`) com `nosnippet`,
       `noarchive`, `noimageindex` ou `max-snippet:N` (incluindo
       `max-snippet:0`, que zera qualquer trecho citável no resultado de
       busca tradicional).
    2. Atributo `data-nosnippet` em qualquer elemento do corpo — marca um
       trecho específico como não-citável mesmo com o resto da página
       liberada.
    3. Header HTTP equivalente (`X-Robots-Tag`) quando informado via
       `--header` (a ferramenta não faz requisição HTTP; se você já tem o
       header em mãos, cole aqui).

    Nenhuma dessas diretivas impede indexação — impedem especificamente que
    um trecho da página seja mostrado como citação (snippet no Google,
    passagem citada por uma IA que respeita a diretiva).

USO
    python anti_citation_directives_check.py pagina.html
    python anti_citation_directives_check.py pagina.html --header "noindex, max-snippet:0"

LIMITAÇÕES
    Não confirma que sistemas de IA de terceiros de fato respeitam essas
    diretivas — cada provedor documenta separadamente quais tags obedece.
    A ferramenta aponta a presença da diretiva no HTML; a decisão de
    manter ou remover é do dono do site.

Autor: Lucas Ferraz (lucasferraz.com) — dependência zero, só biblioteca padrão.
Licença: MIT.
"""
from __future__ import annotations

import argparse
import re
import sys

DIRETIVAS_ANTI_CITACAO = ("nosnippet", "noarchive", "noimageindex")
META_ROBOTS_RE = re.compile(
    r'(?is)<meta\s+[^>]*name=["\'](robots|googlebot|bingbot)["\'][^>]*content=["\']([^"\']*)["\']'
)
MAX_SNIPPET_RE = re.compile(r"max-snippet:\s*(-?\d+)", re.I)
DATA_NOSNIPPET_RE = re.compile(r"(?is)<[a-z0-9]+[^>]*\bdata-nosnippet\b[^>]*>")


def analisa_content(content: str, origem: str, atencoes: list[str]) -> None:
    partes = [p.strip().lower() for p in content.split(",")]
    for d in DIRETIVAS_ANTI_CITACAO:
        if d in partes:
            atencoes.append(f"{origem}: diretiva \"{d}\" (bloqueia citação/snippet de todo o documento)")
    m = MAX_SNIPPET_RE.search(content)
    if m:
        valor = int(m.group(1))
        if valor == 0:
            atencoes.append(f"{origem}: \"max-snippet:0\" (zera qualquer trecho citável)")
        elif valor > 0:
            atencoes.append(f"{origem}: \"max-snippet:{valor}\" (limita o trecho citável a {valor} caracteres)")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Varre HTML atrás de diretivas que bloqueiam citação e snippet."
    )
    ap.add_argument("arquivo", help="arquivo .html")
    ap.add_argument("--header", default="",
                     help="valor do header HTTP X-Robots-Tag, se você já o tiver (a ferramenta não faz requisição)")
    args = ap.parse_args()

    try:
        with open(args.arquivo, encoding="utf-8") as fh:
            html = fh.read()
    except OSError as exc:
        print(f"Não consegui ler {args.arquivo}: {exc}", file=sys.stderr)
        sys.exit(2)

    atencoes: list[str] = []

    for m in META_ROBOTS_RE.finditer(html):
        nome, content = m.group(1), m.group(2)
        analisa_content(content, f"<meta name=\"{nome}\">", atencoes)

    if args.header:
        analisa_content(args.header, "header X-Robots-Tag informado", atencoes)

    data_nosnippet = DATA_NOSNIPPET_RE.findall(html)
    if data_nosnippet:
        atencoes.append(f"{len(data_nosnippet)} elemento(s) com atributo data-nosnippet no corpo")

    print(f"\n=== anti-citation-directives-check: {args.arquivo} ===")
    if not atencoes:
        print("Nenhuma diretiva anti-citação encontrada.")
        sys.exit(0)

    for a in atencoes:
        print("  ATENÇÃO  " + a)
    print("\n(Presença da diretiva, não confirmação de que todo provedor de IA a respeita.)")
    sys.exit(1)


if __name__ == "__main__":
    main()
