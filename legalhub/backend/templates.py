"""Plain-text draft aids. These are not court forms or legal advice."""
SCOTLAND_CLAIM_SUMMARY_TEMPLATE = """DRAFT CASE SUMMARY — FOR REVIEW ONLY
Generated {{ today }}. Not a court form; check facts and procedure independently.

Claimant: {{ claimant.name }}
Address: {{ claimant.address_full }}
Respondent: {{ defendant.name }}
Address: {{ defendant.address_full }}

Issue: {{ claim.dispute_summary_one_liner or claim.claim_type }}
Amount described by user: £{{ '%.2f'|format(claim.amount_claimed) }}

What happened (user's account):
{{ claim.facts_narrative }}

Steps already taken:
{{ claim.pre_action_steps or 'None recorded.' }}

Outcome requested (user's words):
{{ claim.desired_outcome_text }}

Evidence checklist:
{% for item in evidence_items %}- {{ item.label }}{% if item.reference %} ({{ item.reference }}){% endif %}
{% else %}- No evidence items recorded yet.
{% endfor %}
Review names, dates, amounts and supporting evidence before using this draft.
"""

SCHEDULE_OF_LOSS_TEMPLATE = """DRAFT ITEM LIST — NOT A COURT SCHEDULE
Claimant: {{ claimant.name }}
{% for item in loss_items %}- {{ item.label }}: £{{ '%.2f'|format(item.amount) }} ({{ item.date_or_unknown }})
{% else %}- No individual loss items recorded.
{% endfor %}
Item total: £{{ '%.2f'|format(totals.principal) }}
Amount described for claim: £{{ '%.2f'|format(claim.amount_claimed) }}
These figures may differ. Interest, fees and recoverability are not calculated.
"""

TIMELINE_TEMPLATE = """DRAFT EVENT TIMELINE — FOR REVIEW ONLY
{% for event in events %}- {{ event.date }} — {{ event.title }}: {{ event.description }}
{% else %}- No dated events recorded yet.
{% endfor %}
"""

LBC_TEMPLATE = "Letter Before Claim from {{ claimant.name }} to {{ defendant.name }} — placeholder only."
PARTICULARS_TEMPLATE = "Particulars of Claim for {{ claimant.name }} vs {{ defendant.name }} — placeholder only."
