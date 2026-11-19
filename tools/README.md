# DisasterReference tools

## Download originals

```sh
python3 tools/download.py --output downloads
```

This reads the recommended CSV, tries each preferred URL and its listed fallback, checks the response format, and saves the original HTML or PDF. The JSON report records failures, resolved URLs, retrieval timestamps, and SHA-256 hashes. The process exits with a nonzero status when any row fails. Keep the report with the downloads so a later conversion can cite the exact input.

A saved HTML response is the original page source. Review it offline. Linked images, interactive tools, and linked documents may need separate handling, especially for maps and safety instructions.

## Convert one local original

Install the Python dependencies in a virtual environment and install Poppler's `pdftotext` on your system for PDF input.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r tools/requirements.txt
python tools/convert.py downloads/example.html --metadata source.json --output-dir build/example
```

The converter extracts the source once into structured Markdown. The same article supplies the editable Markdown, searchable TXT, EPUB, and the letter, phone, and e-ink PDF layouts. The bundle contains `example.md`, `example.txt`, `example.epub`, `example.pdf`, `example-phone.pdf`, `example-eink.pdf`, and `example.provenance.json`. When the input is a publisher PDF, `example.pdf` contains the exact original bytes. The phone and e-ink files are text adaptations with the library cover and footers. The shared provenance file identifies the original and the conversions.

Use a new output directory for each bundle. The converter makes the directory available after all outputs succeed. Bundles under `build/` are stored locally and ignored by Git.

For one format, use the existing `--format` and `--output` options.

```sh
python tools/convert.py downloads/example.html --metadata source.json --format epub --output build/example.epub
```

The [extraction specification](../docs/extraction.md) lists the metadata fields and the local review required for the resulting text. PDF modes add a **PrepperCache - Disaster Reference Library** source page and a repeating title, source, and page-number footer. Trafilatura extracts Markdown from HTML. Poppler extracts text from PDF by page. Pandoc and Typst render the output. Keep the source and provenance JSON with the export. Review the generated Markdown and representative PDF pages before relying on an extracted copy.

| Mode | Output | Use |
| --- | --- | --- |
| `markdown` | `.md` | Raw editable reading text for review and search. |
| `txt` | `.txt` | Simple searchable text for offline readers. |
| `epub` | `.epub` | Reflowable book for phones and e-ink devices. |
| `pdf` | `.pdf` | US Letter document for printing or a larger reader. |
| `pdf-phone` | `.pdf` | Narrow portrait pages on a 90 × 160 mm layout. |
| `pdf-eink` | `.pdf` | 56 × 93.33 mm portrait pages for a screen in the 4.3-inch class. |

The [Xteink X4 Classic specification](https://www.xteink.com/products/xteink-x4-classic-pocket-ereader) lists EPUB and TXT as document formats and its FAQ describes limitations of PDF support. Start with EPUB on that device. The pocket PDF profile uses the 3:5 aspect ratio of [Survival Codex's 480 × 800 display](https://survivalcodex.com/pages/press). Check fixed-layout PDFs on the actual device or its supported conversion app. Verify text size, page turns, contrast, and tables before using a bundle in the field.

The pilot handles text-oriented HTML and searchable PDFs. OCR, direct ZIM extraction, converting batches of source documents, and device-specific XTC packaging are planned follow-ups. Keep the original available whenever the article depends on illustrations or other material omitted by the text extraction.
