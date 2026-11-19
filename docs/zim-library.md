# Shared ZIM archives

The [archive list](../catalog/zim-archives.csv) starts with 17 English-language ZIMs from PrepperCache. It covers Wikipedia variants, medical references, food preparation, disaster recovery, repair, electronics, and open textbooks. These collections are useful for browsing and deep lookup. The [recommended document list](../catalog/recommended.csv) is the download list for short emergency readings.

The [overlap evidence](../catalog/zim-evidence.csv) records what each comparison source actually lists. PrepperPi names archives in its Starter, Medical, Education, and Complete bundle manifests. Project N.O.M.A.D. publishes versioned collections and Wikipedia options. Lastbook names exact filenames in its pack specification. Prepper Disk's public FAQ names Wikipedia and iFixit without giving filenames. The citations pin public manifests to the inspected commits where available.

## Read the archive list

- `archive_id` is the Kiwix archive identifier without the date or extension. It includes the language and variant when the upstream name specifies them.
- `title`, `category`, `language`, and `description` describe the archive and where it fits in DisasterReference.
- `version`, `size_mb`, and `archive_url` come from the linked PrepperCache catalog snapshot. Size is the catalog estimate. Confirm the current URL and availability before downloading.
- `preppercache_source_url` points to the exact catalog snapshot used for the row.

## Read the overlap evidence

| Match | Meaning |
| --- | --- |
| `same_edition` | The project lists the same archive identifier and version. This compares published metadata. |
| `same_archive` | The archive identifier matches. The edition differs or the project does not specify it. |
| `same_collection` | The project lists the same underlying collection. The archive variant differs or is unspecified. |

Each evidence row gives the other project's archive ID and version when published. Multiple bundles in one project can list the same archive. Use the number of distinct projects when comparing overlap.

Kiwix's Wikipedia `mini` editions contain article introductions and infoboxes. `nopic` keeps the full article text and omits images. `maxi` is the full media edition. Choose one Wikipedia edition for your storage budget, and use the [selected article list](../catalog/wikipedia.csv) for topic-level curation. [Kiwix explanation](https://get.kiwix.org/en/faq-items/what-do-mini-nopic-and-maxi-mean-in-the-wikipedia-zim-files/)
