#!/usr/bin/env python3
# DisasterReference
# Copyright (c) 2026 Aaron Morris / A2ThreeD.
# Repository and project information: README.md

"""Extract a local source once and export it for offline reading."""

import argparse
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import urlsplit

import pypandoc
import trafilatura
import typst

PDF_MODES = ("pdf", "pdf-phone", "pdf-eink")
OUTPUT_ENDINGS = {
    "markdown": ".md",
    "txt": ".txt",
    "epub": ".epub",
    "pdf": ".pdf",
    "pdf-phone": "-phone.pdf",
    "pdf-eink": "-eink.pdf",
}
PDF_LAYOUT = Path(__file__).with_name("pdf_layout.typ")
REDISTRIBUTION_NOTES = {
    "permitted": "Redistribution is permitted under the recorded conditions.",
    "prohibited": "The recorded terms prohibit redistribution.",
    "unverified": "Redistribution permission has not been verified.",
}
RIGHTS_STATES = {"permitted", "prohibited", "unverified"}
HEADER_FIELDS = {
    "title": "Title",
    "credit": "By",
    "source_url": "Source",
    "retrieved_from": "Retrieved from",
    "edition": "Source edition",
    "retrieved_at": "Retrieved at",
    "extracted_at": "Extracted at",
    "sha256": "Source SHA-256",
    "changes": "Scope and changes",
    "rights": "Rights",
    "rights_checked_on": "Rights checked on",
    "extraction": "Extraction",
    "redistribution": "Redistribution",
    "conditions": "Conditions",
}
SOURCE_FIELDS = HEADER_FIELDS.keys() - {"extracted_at", "sha256"}


def read_provenance(path, source_bytes):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Metadata must be a JSON object.")
    for field in SOURCE_FIELDS:
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"Metadata requires a value for {field}.")
    rights = data["extraction"], data["redistribution"]
    if any(state not in RIGHTS_STATES for state in rights):
        raise ValueError("Use permitted, prohibited, or unverified for each rights decision.")
    if data["extraction"] != "permitted":
        raise ValueError("The recorded extraction decision must be permitted to convert a source.")
    date.fromisoformat(data["rights_checked_on"])
    if datetime.fromisoformat(data["retrieved_at"]).tzinfo is None:
        raise ValueError("Provide retrieved_at as an ISO 8601 timestamp with a time zone.")
    checksum = hashlib.sha256(source_bytes).hexdigest()
    if data.get("sha256", checksum) != checksum:
        raise ValueError("The source bytes do not match the acquisition checksum.")
    return {
        **data,
        "sha256": checksum,
        "extracted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def literal(text):
    return re.sub(r"([\\`*_{}\[\]<>#+!|])", r"\\\1", text)


def extract_markdown(suffix, source, workdir, provenance):
    if suffix in {".html", ".htm"}:
        body = trafilatura.extract(
            source, url=provenance["retrieved_from"], output_format="markdown",
            include_comments=False, include_links=True, include_tables=True,
        )
        method = "HTML main text extracted. Images, styling, and interactive content were omitted."
    else:
        if not source.startswith(b"%PDF-"):
            raise ValueError("The input does not start with a PDF signature.")
        copy = workdir / "source.pdf"
        copy.write_bytes(source)
        result = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(copy), "-"],
            check=True, capture_output=True, text=True, encoding="utf-8", timeout=120,
        )
        pages = result.stdout.rstrip("\f").split("\f")
        sections = []
        for number, page in enumerate(pages, 1):
            if page.strip():
                lines = [literal(line.strip()) for line in page.strip().splitlines()]
                sections.append(f"## Source page {number}\n\n" + "  \n".join(lines))
        body = "\n\n".join(sections)
        method = (
            "PDF text extracted by page without OCR. Images and layout were omitted. "
            "Check tables, reading order, and pages with missing text against the source."
        )
    if not body or not body.strip():
        raise ValueError("No readable text was extracted. Check the original for scanned pages or blocked content.")
    provenance["changes"] = f"{provenance['changes']} {method}"
    return body


def sanitize_document(node):
    if isinstance(node, list):
        return [sanitize_document(item) for item in node]
    if isinstance(node, dict):
        kind = node.get("t")
        if kind in {"Image", "Link"}:
            _, label, (target, _) = node["c"]
            if kind == "Image" or (not target.startswith("#") and urlsplit(target).scheme not in {"http", "https"}):
                return {"t": "Span", "c": [["", [], []], sanitize_document(label)]}
        return {key: sanitize_document(value) for key, value in node.items()}
    return node


def render_pdf(document, provenance, mode, workdir, destination, has_body):
    retrieved = datetime.fromisoformat(provenance["retrieved_at"]).astimezone(timezone.utc)
    converted = datetime.fromisoformat(provenance["extracted_at"]).astimezone(timezone.utc)
    dates = f"Retrieved {retrieved:%b %d, %Y}. Converted {converted:%b %d, %Y} (UTC)."
    source_url = provenance["source_url"]
    access_url = provenance["retrieved_from"]
    access_match = re.match(r"https?://([^/?#]+)", access_url)
    access_label = access_match.group(1) if access_match and access_url != source_url else ""
    inputs = {
        "mode": mode,
        "title": provenance["title"],
        "credit": provenance["credit"],
        "source-url": source_url,
        "source-display": source_url,
        "access-url": access_url,
        "access-label": access_label,
        "edition": provenance["edition"].rstrip("."),
        "dates": dates,
        "changes": provenance["changes"],
        "rights": provenance["rights"],
        "reuse": REDISTRIBUTION_NOTES[provenance["redistribution"]],
        "conditions": provenance["conditions"],
        "has-body": "yes" if has_body else "no",
    }
    # Long source URLs and uninterrupted strings must wrap on narrow pages.
    for key in ("title", "credit", "source-display", "access-label", "edition", "changes", "rights", "conditions"):
        inputs[key] = re.sub(r"(\S{18})(?=\S)", r"\1" + "\u200b", " ".join(inputs[key].split()))
    typst.compile(document, output=destination, root=workdir, sys_inputs=inputs)


def parse_markdown(markdown):
    reader = "markdown-raw_html-raw_tex-raw_attribute-yaml_metadata_block"
    parsed = pypandoc.convert_text(markdown, "json", format=reader, extra_args=["--sandbox"])
    return sanitize_document(json.loads(parsed))


def render_outputs(body, provenance, workdir, destinations):
    if any(mode in destinations for mode in ("markdown", "txt", "epub")):
        fields = [
            f"**{label}** — {literal(' '.join(provenance[key].split()))}"
            for key, label in HEADER_FIELDS.items()
        ]
        header = "\n\n".join(fields) + "\n\n---\n\n"
        if "markdown" in destinations:
            markdown = header + body
            destinations["markdown"].write_text(markdown.rstrip() + "\n", encoding="utf-8")
    if destinations.keys() == {"markdown"}:
        return

    document = parse_markdown(body)
    if "txt" in destinations or "epub" in destinations:
        # Keep the same shared article structure and add the visible metadata for reflowable outputs.
        metadata = parse_markdown(header)
        blocks = metadata["blocks"] + document["blocks"]
        payload = json.dumps({**document, "blocks": blocks}, ensure_ascii=False)
        if "txt" in destinations:
            plain = pypandoc.convert_text(
                payload, "plain", format="json", extra_args=["--sandbox", "--wrap=none"],
            )
            destinations["txt"].write_text(plain, encoding="utf-8")
        if "epub" in destinations:
            pypandoc.convert_text(
                payload, "epub3", format="json", outputfile=str(destinations["epub"]),
                extra_args=["--metadata", f"title={provenance['title']}"],
            )

    pdf_modes = [mode for mode in PDF_MODES if mode in destinations]
    if pdf_modes:
        # The same Typst document is compiled against each page profile.
        source = pypandoc.convert_text(
            json.dumps(document, ensure_ascii=False), "typst", format="json",
            extra_args=["--standalone", "--syntax-highlighting=none", "--template", str(PDF_LAYOUT)],
        )
        typst_document = workdir / "document.typ"
        typst_document.write_text(source, encoding="utf-8")
        for mode in pdf_modes:
            render_pdf(typst_document, provenance, mode, workdir, destinations[mode], bool(body.strip()))


def render(body, provenance, mode, workdir, destination):
    render_outputs(body, provenance, workdir, {mode: destination})


def write_provenance(destination, provenance):
    destination.write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def export_bundle(body, provenance, workdir, destination, stem, original_pdf):
    bundle = workdir / "bundle"
    bundle.mkdir()
    outputs = {mode: bundle / (stem + ending) for mode, ending in OUTPUT_ENDINGS.items()}
    renders = outputs.copy()
    if original_pdf is not None:
        renders.pop("pdf").write_bytes(original_pdf)
    render_outputs(body, provenance, workdir, renders)
    record = {
        **provenance,
        "outputs": {
            mode: {
                "filename": path.name,
                "kind": "original" if mode not in renders else "converted",
            }
            for mode, path in outputs.items()
        },
    }
    write_provenance(bundle / (stem + ".provenance.json"), record)
    bundle.rename(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--format", choices=OUTPUT_ENDINGS, help="Single-format export mode")
    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument("--output-dir", type=Path, help="New directory for all offline formats")
    output.add_argument("--output", type=Path, help="Output file for a single format")
    args = parser.parse_args()
    suffix = args.source.suffix.lower()
    if suffix not in {".htm", ".html", ".pdf"}:
        parser.error("Use a local HTML or PDF input.")
    mode = args.format or "markdown"
    destination = args.output_dir if args.output_dir is not None else args.output
    if args.output_dir is not None:
        if args.format:
            parser.error("--format is only used with --output.")
        if destination.exists() or destination.is_symlink():
            parser.error("Choose a new directory for the bundle.")
    else:
        expected_suffix = Path("document" + OUTPUT_ENDINGS[mode]).suffix
        if destination.suffix.lower() != expected_suffix:
            parser.error(f"The selected format requires an output ending in {expected_suffix}.")
        if args.source.resolve() == destination.resolve():
            parser.error("The output must be separate from the source.")
    try:
        source = args.source.read_bytes()
        provenance = read_provenance(args.metadata, source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
            workdir = Path(temporary)
            body = extract_markdown(suffix, source, workdir, provenance)
            if args.output_dir is not None:
                original_pdf = source if suffix == ".pdf" else None
                export_bundle(body, provenance, workdir, destination, args.source.stem, original_pdf)
            else:
                output_file = workdir / f"converted{expected_suffix}"
                render(body, provenance, mode, workdir, output_file)
                sidecar = workdir / "provenance.json"
                write_provenance(sidecar, provenance)
                output_file.replace(destination)
                sidecar.replace(destination.with_name(destination.name + ".provenance.json"))
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"Conversion failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
