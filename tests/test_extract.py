import pytest

from avv_checker.extract import ExtractionError, extract_text


def test_extracts_plain_txt(tmp_path):
    path = tmp_path / "vertrag.txt"
    path.write_text("Gegenstand der Verarbeitung ist die Testdatei.", encoding="utf-8")
    text = extract_text(path)
    assert "Gegenstand der Verarbeitung" in text


def test_missing_file_raises_extraction_error(tmp_path):
    with pytest.raises(ExtractionError):
        extract_text(tmp_path / "existiert-nicht.txt")


def test_unsupported_extension_raises_extraction_error(tmp_path):
    path = tmp_path / "vertrag.xlsx"
    path.write_text("Inhalt", encoding="utf-8")
    with pytest.raises(ExtractionError):
        extract_text(path)


def test_empty_file_raises_extraction_error(tmp_path):
    path = tmp_path / "leer.txt"
    path.write_text("   \n\n  ", encoding="utf-8")
    with pytest.raises(ExtractionError):
        extract_text(path)


def test_extracts_docx(tmp_path):
    docx = pytest.importorskip("docx")
    path = tmp_path / "vertrag.docx"
    document = docx.Document()
    document.add_paragraph("Gegenstand der Verarbeitung ist der Betrieb der Software.")
    table = document.add_table(rows=1, cols=1)
    table.rows[0].cells[0].text = "Dauer der Verarbeitung: 12 Monate."
    document.save(str(path))

    text = extract_text(path)
    assert "Gegenstand der Verarbeitung" in text
    assert "Dauer der Verarbeitung" in text


def test_extracts_pdf(tmp_path):
    pytest.importorskip("reportlab")
    from reportlab.pdfgen import canvas

    path = tmp_path / "vertrag.pdf"
    c = canvas.Canvas(str(path))
    c.drawString(72, 720, "Gegenstand der Verarbeitung ist der Betrieb der Software.")
    c.save()

    text = extract_text(path)
    assert "Gegenstand der Verarbeitung" in text
