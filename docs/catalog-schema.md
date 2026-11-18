# Catalog schema

CSV files use UTF-8, a comma delimiter, a single header row, and standard double-quote escaping. Use blank cells for unknown optional values. Dates use YYYY-MM-DD. IDs use lowercase ASCII letters, digits, and hyphens. Keep IDs stable if URLs or titles change.

## Resources

One row represents a reference in its reviewed edition and language. Choose the best verified copy for offline use or the publisher's web page if that is the only confirmed format. Record materially different editions or translations separately when they need independent review.

| Column | Meaning |
| --- | --- |
| `id` | Stable unique resource ID. |
| `title` | Title as published. |
| `description` | Original one- or two-sentence summary of its practical use. |
| `category` | Primary topic slug from the table below. |
| `resource_type` | Content type such as `checklist`, `guide`, `manual`, `reference`, `map`, or `collection`. |
| `publisher` | Original publishing organization or author. |
| `source_url` | Canonical publisher page for the resource. |
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
