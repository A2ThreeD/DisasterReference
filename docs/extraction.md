# Offline extraction and provenance

Every extracted document starts with visible provenance. Render the compact header before the body in TXT, Markdown, HTML, and EPUB. PDFs use the source page described below. Store the full fields in the provenance sidecar and export manifest so reviewers and tools can inspect them without opening each document.

The following is a template. Replace placeholders with recorded values.

```text
Title: <original title>
By: <author, publisher, or contributor credit>
Source: <canonical URL>
Retrieved from: <actual URL or archive name and entry path>
Source edition: <version, publication date, or revision permalink>
Retrieved at: <UTC timestamp in ISO 8601>
Extracted at: <UTC timestamp in ISO 8601>
Source SHA-256: <hash of the retained source bytes>
Scope and changes: <pages or sections included, omissions, OCR, or edits>
Rights: <license or public-domain basis, with a URL or permission reference>
Rights checked on: <YYYY-MM-DD>
Extraction: <permitted, prohibited, or unverified>
Redistribution: <permitted, prohibited, or unverified>
Conditions: <required credit, license terms, or limits>
```

## PDF export layout

- Use the original publisher's PDF or official print edition when it is available. Preserve its bytes, including its cover, pagination, graphics, and form fields. Record the publisher, download location, and checksum in the export report.
- When the source only provides a web page, convert the verified HTML under the applicable reuse terms. Apply the library source page and footer to the conversion. Keep a source link in the report if the page cannot be converted with its necessary content intact.
- Open every converted PDF with a source page headed **PrepperCache - Disaster Reference Library**. Give the original document title the largest type. Put the author or publisher immediately below it and link to the canonical source.
- Use short labeled sections in plain language. **About this copy** identifies the source edition, retrieval and conversion dates, and any changes or omissions. **Source and reuse** describes attribution, reuse conditions, and the recorded redistribution decision. Link to an alternate retrieval site when used. Keep exact URLs, timestamps, checksums, and the complete rights record in the JSON provenance sidecar.
- Put the document title, credited source, and sequential export page number in a legible footer on every page, including the source page. Body content starts after the provenance. On narrow layouts, lengthy provenance may continue onto another page before the body.

## Input metadata for the converter

Pass a JSON object to [the conversion tool](../tools/README.md) with these string fields. Use the actual source and rights decision. The example uses an original local fixture.

```json
{
  "title": "Fixture title",
  "credit": "Aaron Morris / A2ThreeD",
  "source_url": "https://example.org/resource",
  "retrieved_from": "Local fixture",
  "edition": "Fixture 1",
  "retrieved_at": "2026-11-18T00:00:00Z",
  "changes": "Entire input document.",
  "rights": "Original document, permission recorded by its author.",
  "rights_checked_on": "2026-11-18",
  "extraction": "permitted",
  "redistribution": "unverified",
  "conditions": "Local test use."
}
```

Copy retrieval details and the optional `sha256` from the download report. The tool checks any supplied hash against the source bytes. A single-format export writes its own provenance sidecar. A multi-format bundle records one extraction timestamp and lists each file, its format, and whether it is an original or a conversion in a shared provenance sidecar.

## Rights decisions

Record the rights decision per edition and intended use, with the date it was checked. Track permission to extract and permission to redistribute independently. The downloader can save an authorized original for the reader. Converted copies require a documented basis for extraction, and published bundles require a documented basis for redistribution and compliance with its conditions. Keep the catalog link available while a rights decision is unresolved.

For Wikipedia, credit the article's contributors and retain both the public article URL and the revision permalink. Check the specific article footer, history, and discussion page for imported text or attribution requirements. Include the applicable license notice and URL, indicate the changes, and honor ShareAlike where required. Handle images and other media according to their individual terms. See the [Wikimedia reuse terms](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use#7._Licensing_of_Content) and [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/).

For U.S. federal publications, record whether the material qualifies as a U.S. government work in the intended jurisdiction. Review credited third-party content, co-published material, and any special terms separately. A public release marking identifies the document's distribution status. Record the copyright basis independently. See [17 U.S.C. § 105](https://uscode.house.gov/us/usc/t17/s105/).

For PDFs and ZIMs, record page numbers or article paths. Keep required warnings, units, and diagrams. If the converted copy loses any information needed to use a procedure safely, point to the original and hold the converted copy for review.
