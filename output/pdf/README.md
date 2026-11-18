# PDF library storage

A local PDF export of [the recommended catalog](../../catalog/recommended.csv) lives here. Open `index.pdf` to browse in catalog order, or use `export-report.csv` to see the output path, source URL, retrieval date, checksums, and status for every item.

| Location | Contents |
| --- | --- |
| `prepare/<category>/` | Household preparation PDFs, organized by topic. |
| `reference/<category>/` | Emergency and recovery PDFs, organized by topic. |
| `index.pdf` | Printable index with local paths and online source links. |
| `export-report.csv` | Export status, provenance, and source links for every recommended entry. |

Publisher PDFs and printable access copies retain their original pages, diagrams, and form fields. Converted pages have a visible source and rights header plus a provenance JSON file. Download and convert using the [local tools](../../tools/README.md). Keep the original format whenever a conversion would omit information needed for offline use, such as a map legend or an interactive worksheet. When a printable copy is unavailable, keep the source link in the report.

Git tracks this layout and its documentation. The generated collection is stored locally. Review rights and redistribution conditions per item before publishing any bundle. See [extraction and provenance](../../docs/extraction.md).
