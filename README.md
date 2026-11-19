# DisasterReference

DisasterReference is built to be a small repository of quality review information that someone would use for core Disaster Prep and Survival information. This repository and its tools are meant to take publicly available sourced information and create printable PDF and text documents that can be used on any device.

The first release will aim for a short, broadly applicable list, with additional references for specific hazards, regions, and equipment. Each recommendation will point back to the publisher and show the evidence behind its inclusion. The catalog will use categories familiar to [PrepperCache](https://github.com/A2ThreeD/PrepperCache) so that I can integrate these documents into it as well.

## Start here

Use the [recommended download list](catalog/recommended.csv) to save the starter library in one pass. It is the entry point for both readers and AI agents. See [download instructions](docs/downloading.md) for file handling and fallbacks.

Open the [first readings by task and category](docs/start-here.md) for the initial browsing draft. Each category aims for three to five concise core documents, with room for fewer when the evidence supports a shorter list. Larger references are available below the first readings.

- [Resources CSV](catalog/resources.csv) records titles, descriptions, topics, links, formats, editions, and review status.
- [Evidence CSV](catalog/evidence.csv) links each resource to the sources that recommend or discuss it.
- [Shared ZIM archive catalog](docs/zim-library.md) records PrepperCache archives with overlap evidence from other projects.
- [Wikipedia CSV](catalog/wikipedia.csv) lists a focused set of background articles by category.
- [Maintainer review log](catalog/reviews.csv) records confirmed decisions to keep, update, remove, or promote documents.
- [Download and conversion tools](tools/README.md) provide a local workflow for HTML, PDF, Markdown, TXT, EPUB, and device-sized PDFs.
- [Public offline exports](published/README.md) links to cleared PDFs and device bundles.
- [Local PDF library storage](output/pdf/README.md) describes the category folders, index, and export report.
- [Extraction specification](docs/extraction.md) defines the source and rights information to include in offline conversions.
- [Catalog schema](docs/catalog-schema.md) explains categories and how to add records.
- [Source review](docs/source-review.md) tracks the six comparison projects and what their public material establishes.
- [Editorial method](docs/editorial-method.md) explains how candidates are compared and how the core list is selected.
- [Roadmap](docs/roadmap.md) covers the initial research and offline exports.
- [Contributor and agent instructions](AGENTS.md) apply to work in this repository.

The initial catalog contains publisher-checked candidates and evidence from public project material. The core tier includes the maintainer-selected [Building Wilderness Shelter guide](published/pdf/reference/survival-shelter/building-wilderness-shelter.pdf). The repository catalogs third-party references by link. Rights for source documents and derived exports must be tracked per resource.

## Contribute a source

Open an issue with the original URL, publisher, the resource or topic it covers, and where the recommendation appears. Include the edition, intended audience, region, and any known access or reuse terms when available. A link to a whole preparedness library is also welcome. Identify specific documents or sections whenever you can.
