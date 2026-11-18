#!/usr/bin/env python3
# DisasterReference
# Copyright (c) 2026 Aaron Morris / A2ThreeD.
# Repository and project information: README.md

"""Download the recommended originals and record acquisition provenance."""

import argparse
import csv
from datetime import datetime, timezone
import hashlib
from http.client import HTTPException
import json
from pathlib import Path
import re
import tempfile
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
FORMATS = {"html", "pdf"}
MAX_BYTES = 64 * 1024 * 1024


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_manifest(path):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    names = set()
    for row in rows:
        name, fmt = row["filename"], row["format"]
        if fmt not in FORMATS or not re.fullmatch(r"[a-z0-9][a-z0-9-]*\." + fmt, name):
            raise ValueError(f"Invalid format or filename: {name}")
        if name in names:
            raise ValueError(f"Duplicate filename: {name}")
        names.add(name)
        for url in (row["url"], row["fallback_url"]):
            if url and (urlsplit(url).scheme != "https" or not urlsplit(url).hostname):
                raise ValueError(f"Expected an HTTPS URL: {url}")
        if not row["url"]:
            raise ValueError(f"Missing download URL: {name}")
    return rows


def fetch(url, destination, fmt, timeout):
    request = Request(url, headers={"User-Agent": "DisasterReference/1.0"})
    digest = hashlib.sha256()
    with urlopen(request, timeout=timeout) as response:
        resolved = response.geturl()
        if urlsplit(resolved).scheme != "https":
            raise ValueError("The server redirected to a non-HTTPS URL.")
        prefix = response.read(32768)
        looks_like_html = re.search(rb"<(?:!doctype html|html[\s>])", prefix, re.I)
        if fmt == "pdf" and not prefix.startswith(b"%PDF-"):
            raise ValueError("The response does not start with a PDF signature.")
        if fmt == "html" and (response.headers.get_content_type() != "text/html" or not looks_like_html):
            raise ValueError("The response is not an HTML document.")
        with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as handle:
            temporary = Path(handle.name)
            try:
                size = 0
                chunk = prefix
                while chunk:
                    size += len(chunk)
                    if size > MAX_BYTES:
                        raise ValueError("The response exceeded the 64 MiB limit.")
                    handle.write(chunk)
                    digest.update(chunk)
                    chunk = response.read(65536)
                handle.close()
                temporary.replace(destination)
            finally:
                temporary.unlink(missing_ok=True)
    return {"retrieved_from": resolved, "retrieved_at": utc_now(), "sha256": digest.hexdigest()}


def download(row, output, timeout):
    record = {key: row[key] for key in ("resource_id", "title", "filename", "format", "url")}
    errors = []
    for url in (row["url"], row["fallback_url"]):
        if not url:
            continue
        try:
            metadata = fetch(url, output / row["filename"], row["format"], timeout)
        except (HTTPException, OSError, ValueError) as exc:
            errors.append({"url": url, "error": str(exc)})
            continue
        return {**record, **metadata, "status": "saved", "errors": errors}
    return {**record, "status": "failed", "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "catalog" / "recommended.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "downloads")
    parser.add_argument("--timeout", type=float, default=15, help="Network timeout in seconds")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive.")
    try:
        rows = read_manifest(args.manifest)
        args.output.mkdir(parents=True, exist_ok=True)
    except (KeyError, OSError, ValueError) as exc:
        parser.error(str(exc))
    results = []
    for row in rows:
        result = download(row, args.output, args.timeout)
        results.append(result)
        print(f"{result['status']}: {row['filename']}", flush=True)
    log = args.output / "download-report.json"
    log.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Download report: {log}")
    return int(any(row["status"] == "failed" for row in results))


if __name__ == "__main__":
    raise SystemExit(main())
