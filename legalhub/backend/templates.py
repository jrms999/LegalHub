# Minimal placeholder templates – extend as needed with Jinja2 syntax

SCOTLAND_CLAIM_SUMMARY_TEMPLATE = "Simple Procedure Claim Summary for {{ claimant.name }} vs {{ defendant.name }}"

SCHEDULE_OF_LOSS_TEMPLATE = "Schedule of loss for {{ claimant.name }} (total £{{ totals.principal }})"

TIMELINE_TEMPLATE = "Timeline of events for {{ claimant.name }} vs {{ defendant.name }}"

LBC_TEMPLATE = "Letter Before Claim from {{ claimant.name }} to {{ defendant.name }}"

PARTICULARS_TEMPLATE = "Particulars of Claim for {{ claimant.name }} vs {{ defendant.name }}"
