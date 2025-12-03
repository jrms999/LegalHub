"use client";

import React from "react";
import { ClaimWizard } from "./ClaimWizard";
import { createClaim, generateDocuments } from "../lib/api";

export function EnglandWalesWizard() {
  const [form, setForm] = React.useState({
    claimantName: "",
    claimantAddress: "",
    defendantName: "",
    defendantAddress: "",
    amount_claimed: 0,
    summary: "",
    facts_summary: "",
    desired_outcome: "",
    pre_action_steps: ""
  });

  const [saving, setSaving] = React.useState(false);
  const [result, setResult] = React.useState<string | null>(null);

  async function handleSubmit() {
    setSaving(true);
    setResult(null);
    try {
      const payload = {
        jurisdiction: "ENGLAND_WALES",
        claim_type: "MONEY",
        amount_claimed: Number(form.amount_claimed),
        interest_requested: false,
        interest_rate: null,
        interest_from: null,
        facts_summary: form.facts_summary,
        desired_outcome: form.desired_outcome,
        pre_action_steps: form.pre_action_steps,
        dispute_summary_one_liner: form.summary,
        court_name: "",
        parties: [
          {
            role: "CLAIMANT",
            is_company: false,
            name: form.claimantName,
            address_line1: form.claimantAddress,
            address_line2: "",
            town_city: "",
            postcode: "",
            email: "",
            phone: "",
            other_names: ""
          },
          {
            role: "DEFENDANT",
            is_company: false,
            name: form.defendantName,
            address_line1: form.defendantAddress,
            address_line2: "",
            town_city: "",
            postcode: "",
            email: "",
            phone: "",
            other_names: ""
          }
        ],
        events: [],
        loss_items: [],
        evidence_items: []
      };

      const claim = await createClaim(payload);
      const gen = await generateDocuments(claim.id);
      setResult(
        `Claim ${claim.id} created. Generated docs: ${gen.generated.join(", ")}`
      );
    } catch (err: any) {
      setResult(`Error: ${err.message}`);
    } finally {
      setSaving(false);
    }
  }

  const steps = [
    <div key="e1" className="space-y-4">
      <h2 className="text-xl font-semibold">Letter Before Claim – parties</h2>
      <input
        className="border rounded w-full p-2"
        placeholder="Your name"
        value={form.claimantName}
        onChange={(e) =>
          setForm({ ...form, claimantName: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Your address (single line for now)"
        value={form.claimantAddress}
        onChange={(e) =>
          setForm({ ...form, claimantAddress: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Defendant name"
        value={form.defendantName}
        onChange={(e) =>
          setForm({ ...form, defendantName: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Defendant address"
        value={form.defendantAddress}
        onChange={(e) =>
          setForm({ ...form, defendantAddress: e.target.value })
        }
      />
    </div>,
    <div key="e2" className="space-y-4">
      <h2 className="text-xl font-semibold">About the dispute</h2>
      <input
        className="border rounded w-full p-2"
        placeholder="One-line summary"
        value={form.summary}
        onChange={(e) =>
          setForm({ ...form, summary: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        type="number"
        placeholder="Amount claimed (GBP)"
        value={form.amount_claimed}
        onChange={(e) =>
          setForm({ ...form, amount_claimed: Number(e.target.value) })
        }
      />
      <textarea
        className="border rounded w-full p-2"
        rows={5}
        placeholder="What happened?"
        value={form.facts_summary}
        onChange={(e) =>
          setForm({ ...form, facts_summary: e.target.value })
        }
      />
      <textarea
        className="border rounded w-full p-2"
        rows={3}
        placeholder="What do you want the defendant to do?"
        value={form.desired_outcome}
        onChange={(e) =>
          setForm({ ...form, desired_outcome: e.target.value })
        }
      />
      <textarea
        className="border rounded w-full p-2"
        rows={3}
        placeholder="What have you done already to resolve this?"
        value={form.pre_action_steps}
        onChange={(e) =>
          setForm({ ...form, pre_action_steps: e.target.value })
        }
      />

      <button
        type="button"
        onClick={handleSubmit}
        disabled={saving}
        className="px-4 py-2 bg-emerald-600 text-white rounded"
      >
        {saving ? "Saving..." : "Save & generate LBC / particulars"}
      </button>

      {result && <p className="text-sm text-slate-700 mt-2">{result}</p>}
    </div>
  ];

  return <ClaimWizard steps={steps} />;
}
