# anti-citation-directives-check — ferramenta grátis e de código aberto para achar diretiva que bloqueia citação

`anti-citation-directives-check` é uma ferramenta gratuita e de código
aberto que varre um HTML atrás de diretivas que bloqueiam citação e
snippet, e que às vezes acabam na página sem o dono perceber — herdadas de
template, plugin de SEO mal configurado, ou copiadas de outro projeto.

## O problema que ela resolve

`noindex` impede indexação. `nosnippet`, `noarchive`, `max-snippet:0` e
`data-nosnippet` são diferentes: a página pode continuar indexada e
aparecendo na busca, só sem trecho citável no resultado — e, por extensão,
sem o texto disponível para um sistema de IA que respeita essas diretivas
usar como passagem de resposta. É um jeito silencioso de sabotar a própria
citabilidade sem perceber.

## O que a ferramenta verifica

1. `<meta name="robots">` (e as variantes `googlebot`, `bingbot`) com
   `nosnippet`, `noarchive`, `noimageindex` ou `max-snippet:N`.
2. O atributo `data-nosnippet` em qualquer elemento do corpo, que marca um
   trecho específico como não-citável mesmo com o resto da página
   liberada.
3. Opcionalmente, um header HTTP `X-Robots-Tag` que você já tenha em mãos.

## Instalação

Só biblioteca padrão do Python (3.9 ou mais recente). Sem dependência
externa.

```bash
git clone https://github.com/lucasferrazseo/anti-citation-directives-check.git
cd anti-citation-directives-check
```

## Como usar, passo a passo

**1. Rode contra o HTML da página.**

```bash
python anti_citation_directives_check.py pagina.html
```

**2. Leia o relatório.** Exemplo real, de uma página com três diretivas
diferentes:

```
=== anti-citation-directives-check: pagina-nosnippet.html ===
  ATENÇÃO  <meta name="robots">: diretiva "nosnippet" (bloqueia citação/snippet de todo o documento)
  ATENÇÃO  <meta name="robots">: "max-snippet:0" (zera qualquer trecho citável)
  ATENÇÃO  1 elemento(s) com atributo data-nosnippet no corpo

(Presença da diretiva, não confirmação de que todo provedor de IA a respeita.)
```

**3. Confira também o header HTTP**, se você já tiver capturado o
`X-Robots-Tag` de uma resposta (por exemplo, com `curl -I`):

```bash
curl -sI https://exemplo.com/pagina/ | grep -i x-robots-tag
python anti_citation_directives_check.py pagina.html --header "noindex, max-snippet:0"
```

**4. Página sem nenhuma diretiva** retorna direto "nenhuma diretiva
encontrada" e código de saída 0 — útil para checagem em lote via script.

## Perguntas frequentes

**anti-citation-directives-check é realmente grátis?**
Sim, código aberto sob licença MIT.

**Encontrar `nosnippet` significa que o site fez algo errado?**
Não necessariamente — às vezes a diretiva está ali de propósito (conteúdo
sensível, página que não deveria aparecer como trecho citável). A
ferramenta aponta a presença, a decisão de manter ou remover é sua.

**A ferramenta confirma que o Google ou uma IA respeitou a diretiva?**
Não. Aponta o que está declarado no HTML; cada provedor documenta
separadamente quais diretivas de fato respeita.

## Limitações

A ferramenta aponta a presença da diretiva no HTML, não confirma que todo
provedor de IA de terceiro de fato a respeita — cada um documenta
separadamente quais tags obedece.

## Autor

[Lucas Ferraz](https://lucasferraz.com) — especialista em SEO, criação de
sites e SEO para IA, fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT — ver [LICENSE](LICENSE).
