**English** · [Português (Brasil)](README.pt-BR.md)

# anti-citation-directives-check

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

`anti-citation-directives-check` is a free, open source tool that scans an
HTML file for directives that block citation and snippets. These
directives sometimes end up on a page without the owner noticing,
inherited from a template, a misconfigured SEO plugin, or copied from
another project. It runs locally and makes no HTTP requests.

## Contents

- [Background](#background)
- [What it checks](#what-it-checks)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Background

`noindex` blocks indexing. `nosnippet`, `noarchive`, `max-snippet:0` and
`data-nosnippet` are different: the page can stay indexed and keep showing
up in search, just without a quotable snippet in the result. By
extension, the text is also unavailable as an answer passage for an AI
system that honors these directives. It is a silent way to undermine your
own citability without noticing.

## What it checks

1. `<meta name="robots">` (and the `googlebot` and `bingbot` variants)
   with `nosnippet`, `noarchive`, `noimageindex` or `max-snippet:N`.
2. The `data-nosnippet` attribute on any element in the body, which marks
   a specific passage as not quotable even when the rest of the page is
   open.
3. Optionally, an `X-Robots-Tag` HTTP header value you already have.

## Installation

Python 3.9 or newer, standard library only. No external dependencies.

```bash
git clone https://github.com/LucasFerrazSEO/anti-citation-directives-check.git
cd anti-citation-directives-check
```

## Usage

**1. Run it against the page HTML.**

```bash
python anti_citation_directives_check.py pagina.html
```

**2. Read the report.** Real output from a page with three different
directives. The tool prints its report in Brazilian Portuguese.

```
=== anti-citation-directives-check: pagina-nosnippet.html ===
  ATENÇÃO  <meta name="robots">: diretiva "nosnippet" (bloqueia citação/snippet de todo o documento)
  ATENÇÃO  <meta name="robots">: "max-snippet:0" (zera qualquer trecho citável)
  ATENÇÃO  1 elemento(s) com atributo data-nosnippet no corpo

(Presença da diretiva, não confirmação de que todo provedor de IA a respeita.)
```

**3. Also check the HTTP header** if you have already captured the
`X-Robots-Tag` from a response (for example with `curl -I`):

```bash
curl -sI https://exemplo.com/pagina/ | grep -i x-robots-tag
python anti_citation_directives_check.py pagina.html --header "noindex, max-snippet:0"
```

**4. A page with no directives** prints "Nenhuma diretiva anti-citação
encontrada." and exits with code 0 (code 1 when a directive is found),
which is useful for batch checks in a script.

## FAQ

**Is anti-citation-directives-check really free?**
Yes. It is open source under the MIT license.

**Does finding `nosnippet` mean the site did something wrong?**
Not necessarily. Sometimes the directive is there on purpose (sensitive
content, a page that should not appear as a quotable snippet). The tool
points out that it is there; the decision to keep or remove it is yours.

**Does the tool confirm that Google or an AI honored the directive?**
No. It reports what is declared in the HTML; each provider documents
separately which directives it actually honors.

## Limitations

The tool reports the presence of the directive in the HTML. It does not
confirm that every third-party AI provider actually honors it; each one
documents separately which tags it follows.

## Contributing

Bug reports and suggestions are welcome through [GitHub Issues](https://github.com/LucasFerrazSEO/anti-citation-directives-check/issues).

## Author

[Lucas Ferraz](https://lucasferraz.com) is an SEO, website development and Generative Engine Optimization specialist and the founder of [Lucas Ferraz SEO](https://lucasferrazseo.com).

## License

MIT. See [LICENSE](LICENSE).
