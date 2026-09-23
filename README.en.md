# avv-checker

[Deutsche Version](README.md)

avv-checker scans the text of a data processing agreement (Auftragsverar-
beitungsvertrag, AVV under German/EU practice) for wording that typically
covers the 17 contract contents required by Art. 28(2)–(4) GDPR, and
reports which of them could not be found. It reads .txt, .docx, and .pdf
files.

A match only shows that wording matching a given required element is
present, not that it is substantively sufficient. The absence of a match
does not reliably show that a point is unregulated, if unusual wording was
used. The tool does not replace a legal review or advice from a qualified
professional. The full methodology and its limits are in
[METHODIK.md](METHODIK.md) (German).

## Installation

```bash
git clone https://github.com/milaimdelija/avv-checker.git
cd avv-checker
pip install -e .
```

Python 3.10 or newer is required.

## Usage

```bash
avv-checker contract.pdf --out reports/ --format md,html,json
```

This writes `avv-bericht.md`, `avv-bericht.html`, and `avv-bericht.json`
(report file names stay German) to the given directory, and lists any
missing required elements on the command line.

## Local demonstration

`tests/fixtures/` contains two entirely fictional sample contracts:
`sample_avv_complete.txt` covers all 17 required elements,
`sample_avv_incomplete.txt` deliberately omits four of them. Run both with:

```bash
python3 scripts/demo.py
```

Reports are written to `demo_output/`.

## Code layout

`requirements.py` holds the 17 required elements with their search
patterns, `extract.py` reads text from .txt, .docx, and .pdf files,
`matcher.py` checks the extracted text against the requirements, and
`report.py` builds the reports from that. This separation lets the
detection logic be tested in `tests/` without needing sample files in every
format.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT, see [LICENSE](LICENSE).
