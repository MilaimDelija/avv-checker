"""avv-checker: wortlautbasierte Prüfung eines Auftragsverarbeitungsvertrags
(AVV) auf die in Art. 28 Abs. 2 bis 4 DSGVO vorgeschriebenen Vertragsinhalte.

Das Werkzeug durchsucht den Text eines vorgelegten Vertrags nach
Formulierungen, die üblicherweise die einzelnen Pflichtinhalte abdecken, und
meldet, welche davon nicht auffindbar sind. Es bewertet nicht, ob ein
gefundener Passus inhaltlich ausreicht, und ersetzt keine rechtliche
Prüfung. Methodik und Grenzen stehen in METHODIK.md.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("avv-checker")
except PackageNotFoundError:  # Paket lokal aus dem Quellverzeichnis genutzt
    __version__ = "1.0.0"

__all__ = ["__version__"]
