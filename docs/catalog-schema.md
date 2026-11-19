# Catalog schema

CSV files use UTF-8, a comma delimiter, a single header row, and standard double-quote escaping. Use blank cells for unknown optional values. Dates use YYYY-MM-DD. IDs use lowercase ASCII letters, digits, and hyphens. Keep IDs stable if URLs or titles change.

## Resources

One row represents a reference in its reviewed edition and language. Prefer the publisher's PDF or official printable edition for offline use. Record the publisher's web page when a publisher PDF is unavailable. Record materially different editions or translations separately when they need independent review.

| Column | Meaning |
| --- | --- |
| `id` | Stable unique resource ID. |
| `title` | Title as published. |
| `description` | Original one- or two-sentence summary of its practical use. |
| `category` | Primary topic slug from the table below. |
| `resource_type` | Content type such as `checklist`, `guide`, `manual`, `reference`, `map`, or `collection`. |
| `publisher` | Original publishing organization or author. |
| `source_url` | Canonical publisher page, or a documented access page for a historical or archived resource. |
| `asset_url` | Optional direct download URL for the chosen copy. |
| `format` | Format of the asset URL when present, otherwise of the source URL. Use `html`, `pdf`, `zim`, `epub`, `txt`, `markdown`, `pmtiles`, or `other`. |
| `language` | Language tag such as `en` or `es`. |
| `jurisdiction` | Region to which guidance applies, or `global` where that scope is verified. |
| `edition` | Publisher's version, edition, or revision date as displayed. |
| `rights` | Verified license identifier or `unknown`. Use `custom` for terms documented by the publisher. |
| `rights_url` | Optional URL documenting the rights or terms. |
| `tier` | `unassigned`, `core`, or `situational`. |
| `status` | `candidate`, `reviewed`, or `retired`. Only reviewed resources may have a recommendation tier. |
| `checked_on` | Date the record was last verified. |
| `notes` | Selection rationale, limitations, replacement ID, or other review details. |

Require title, description, category, resource type, source URL, format, tier, and status for candidates. Require verified publisher, language, and check date to mark a row reviewed. Record unknown rights explicitly.

## Evidence

Each row records an observation about one resource from one source. Add separate rows where sources independently recommend the same work.

| Column | Meaning |
| --- | --- |
| `resource_id` | Matching resource ID in the resources CSV. |
| `source_name` | Name of the recommending project, publisher, or reviewing organization. |
| `evidence_url` | Page, permalink, or document containing the evidence. |
| `locator` | Section, page number, timestamp, or entry title that makes the evidence easy to find. |
| `independence_group` | Stable slug for the originating organization or recommendation lineage. Leave blank if independence is unresolved. |
| `evidence_type` | `recommends_resource`, `supports_topic`, `lists_resource`, or `raises_concern`. |
| `checked_on` | Date the evidence was inspected. |
| `notes` | Brief paraphrase, edition ambiguity, or relationship to another evidence source. |

Use all fields except `independence_group` and `notes` for every evidence record. For evidence of a recommendation to count toward the core tier, its independence group must be established.

## Recommended downloads

One row per item in the starter download set. The manifest is self-contained for download agents. Keep its title, category, jurisdiction, format, and URLs in sync with the resource catalog. Use reviewed access copies for fallbacks and document the edition or snapshot.

| Column | Meaning |
| --- | --- |
| `resource_id` | Matching ID in the resources CSV. |
| `phase` | `prepare` or `reference`. Preparation rows come first. |
| `category` | Primary topic slug from the table below. |
| `title` | Document title. |
| `jurisdiction` | Geographic scope from the resource record. |
| `format` | Expected format of the downloaded document. |
| `url` | Preferred direct download or HTML page URL. |
| `fallback_url` | Optional same-format access copy to try if the preferred URL fails. |
| `filename` | Suggested local basename with the appropriate file extension. |

## Wikipedia articles

One row per article selected for background reading. Include a task or question the article helps with. Prefer primary sources for instructions with safety consequences. Save a specific revision permalink when extracting an article.

| Column | Meaning |
| --- | --- |
| `id` | Stable article ID prefixed with `wiki-`. |
| `category` | Primary topic slug from the table below. |
| `title` | Article title. |
| `article_url` | Canonical Wikipedia article URL. |
| `use_case` | Task or question the article helps with. |
| `language` | Language tag for the Wikipedia edition. |
| `checked_on` | Date the URL and topic fit were checked. |

## Human review

The [review log](../catalog/reviews.csv) stores dated review decisions keyed by resource ID. See [maintainer review](reviewing.md) for its fields and the update workflow.

## Topic categories

| Slug | Label | PrepperCache counterpart |
| --- | --- | --- |
| `medical` | Medical & First Aid | Medical & First Aid |
| `food-water` | Food and Water | Food and Water |
| `survival-shelter` | Survival & Shelter | Survival & Shelter |
| `repair` | Repair | Repair |
| `communication` | Communication | Communication |
| `power-energy` | Power and Energy | Power and Energy |
| `offline-maps` | Offline Maps | Offline Maps |
| `education-skills` | Education & Skills | Education & Skills |

Choose the category that best represents the resource's main use. The general emergency planning and recovery references start under Survival & Shelter. Wikipedia and other collections can be cataloged under the topic they serve.
