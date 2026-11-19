# PDF library storage

A local PDF export of [the recommended catalog](../../catalog/recommended.csv) lives here. Open `index.pdf` to browse in catalog order, or use `export-report.csv` to see the output path, source URL, retrieval date, checksums, and status for every item.

| Location | Contents |
| --- | --- |
| `prepare/<category>/` | Household preparation PDFs, organized by topic. |
| `reference/<category>/` | Emergency and recovery PDFs, organized by topic. |
| `index.pdf` | Printable index with local paths and online source links. |
| `export-report.csv` | Export status, offline title, provenance, source links, and available bundle paths. |
| `../../build/offline-library/` | Local multi-format bundles for text-oriented conversions. |

Use the publisher’s PDF when available. Store it as supplied, with its original pages, diagrams, and form fields. When the publisher supplies only a web page, convert it following the [PDF export layout](../../docs/extraction.md#pdf-export-layout). Converted PDFs open with a PrepperCache - Disaster Reference Library source page and have title, source, and page-number footers. Each has a provenance JSON file. Download and convert using the [local tools](../../tools/README.md). Keep the original format whenever a conversion would omit information needed for offline use, such as a map legend or an interactive worksheet. When a printable copy is unavailable, keep the source link in the report.

When a companion is used for offline reading, the index shows its actual title and keeps the catalog page available through the source link. The report records both titles and the exact copy used.

Git tracks this layout and its documentation. The complete local collection is stored here. The [public export directory](../../published/README.md) contains copies with documented redistribution terms. Review rights and redistribution conditions per item before publishing any bundle. See [extraction and provenance](../../docs/extraction.md).
