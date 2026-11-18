# Maintainer review

Use [the human review log](../catalog/reviews.csv) to record Aaron Morris's review or another review authorized by the maintainer. Enter one row per review and keep previous decisions as history. The log starts empty.

| Column | Meaning |
| --- | --- |
| `resource_id` | Stable ID from the resource catalog. |
| `reviewer` | Person who actually performed the review. |
| `reviewed_on` | Date in YYYY-MM-DD. |
| `decision` | `keep`, `revise`, `remove`, or `promote_core`. |
| `notes` | Reason, reviewed edition, any limits, or suggested replacement. |

A review can confirm the current download, request edits, remove it from the default list, or promote it to the formal core tier after the [editorial criteria](editorial-method.md) are met. To remove or replace a document, update the [recommended download manifest](../catalog/recommended.csv) and [first-readings page](start-here.md) together. Keep the resource and evidence records for traceability. Set the status to retired when a resource is superseded or withdrawn. When adding a document, record its source and evidence before updating the starter list.

Automated URL checks and research belong in the resource and evidence CSVs. Add a human review row only when the named person confirms their decision.
