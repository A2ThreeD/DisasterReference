// DisasterReference
// Copyright (c) 2026 Aaron Morris / A2ThreeD.
// Project information: README.md

#let metadata = sys.inputs
#let pocket = metadata.mode == "pdf-eink"
#let phone = metadata.mode == "pdf-phone"
#let profile = if pocket {
  (width: 56mm, height: 93.33mm, margin: (x: 4mm, top: 5mm, bottom: 15mm))
} else if phone {
  (width: 90mm, height: 160mm, margin: (x: 6mm, top: 7mm, bottom: 14mm))
} else {
  (paper: "us-letter", margin: (x: 18mm, top: 18mm, bottom: 18mm))
}
#let ink = rgb("#17282d")
#let accent = rgb("#0a634f")
#let footer-size = if pocket { 5.5pt } else if phone { 7pt } else { 8pt }
#let document-footer = context {
  set text(size: footer-size, fill: ink)
  set par(leading: .2em)
  line(length: 100%, stroke: .4pt + gray)
  v(if pocket { 1pt } else { 2pt })
  grid(
    columns: (1fr, auto),
    column-gutter: if pocket { 4pt } else { 9pt },
    align: (left + top, right + top),
    stack(
      dir: ttb,
      spacing: .5pt,
      text(weight: "semibold", metadata.title),
      text("Source: " + metadata.credit),
    ),
    [Page #counter(page).display()],
  )
}

#set document(title: metadata.title, author: metadata.credit)
#set page(..profile, footer: document-footer, footer-descent: 12%)
#set text(size: 10pt, fill: ink)
#set par(justify: false)
#set table(inset: 3pt)
#let horizontalrule = line(length: 100%)
#let title-size = if pocket { 14pt } else if phone { 21pt } else { 29pt }
#let cover-space = if pocket { 4pt } else if phone { 8pt } else { 14pt }
#let detail-size = if pocket { 7.5pt } else if phone { 9pt } else { 11pt }
#let source-label = if metadata.source-url.starts-with("https://") or metadata.source-url.starts-with("http://") {
  link(metadata.source-url, metadata.source-display)
} else {
  metadata.source-display
}

#block(spacing: cover-space)[
  #text(size: if pocket { 8pt } else { 12pt }, weight: "semibold", fill: accent)[Disaster Reference Library]
  #v(cover-space)
  #text(size: title-size, weight: "bold", metadata.title)
  #linebreak()
  #text(size: if pocket { 9pt } else { 13pt }, weight: "semibold", metadata.credit)
  #linebreak()
  #text(size: detail-size, fill: accent, source-label)
  #if metadata.access-label != "" {
    linebreak()
    text(size: detail-size, fill: accent)[Retrieved via #link(metadata.access-url, metadata.access-label)]
  }
]
#block(spacing: cover-space)[
  #set text(size: detail-size)
  #strong[About this copy]
  #linebreak()
  #metadata.edition. #metadata.dates

  #metadata.changes
]
#block(spacing: cover-space)[
  #set text(size: detail-size)
  #strong[Source and reuse]
  #linebreak()
  #metadata.rights

  Conversion was approved. #metadata.reuse #metadata.conditions
]
#if metadata.has-body == "yes" { pagebreak(weak: true) }

$body$
