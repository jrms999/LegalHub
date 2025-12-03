"use client";

import React from "react";
import { ClaimWizard } from "./ClaimWizard";
import { createClaim, generateDocuments } from "../lib/api";

export function ScotlandWizard() {
  const [claimant, setClaimant] = React.useState({
    name: "",
    address_line1: "",
    town_city: "",
    postcode: "",
    email: "",
    phone: ""
  });

  const [defendant, setDefendant] = React.useState({
    name: "",
    address_line1: "",
    town_city: "",
    postcode: "",
    email: "",
    phone: ""
  });

  const [claimInfo, setClaimInfo] = React.useState({
    claim_type: "DEBT",
    amount_claimed: 0,
    dispute_summary_one_liner: "",
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
        jurisdiction: "SCOTLAND",
        claim_type: claimInfo.claim_type,
        amount_claimed: Number(claimInfo.amount_claimed),
        interest_requested: false,
        interest_rate: null,
        interest_from: null,
        facts_summary: claimInfo.facts_summary,
        desired_outcome: claimInfo.desired_outcome,
        pre_action_steps: claimInfo.pre_action_steps,
        dispute_summary_one_liner: claimInfo.dispute_summary_one_liner,
        court_name: "",
        parties: [
          {
            role: "CLAIMANT",
            is_company: false,
            name: claimant.name,
            address_line1: claimant.address_line1,
            address_line2: "",
            town_city: claimant.town_city,
            postcode: claimant.postcode,
            email: claimant.email,
            phone: claimant.phone,
            other_names: ""
          },
          {
            role: "DEFENDANT",
            is_company: false,
            name: defendant.name,
            address_line1: defendant.address_line1,
            address_line2: "",
            town_city: defendant.town_city,
            postcode: defendant.postcode,
            email: defendant.email,
            phone: defendant.phone,
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
    <div key="s1" className="space-y-4">
      <h2 className="text-xl font-semibold">About you (claimant)</h2>
      <input
        className="border rounded w-full p-2"
        placeholder="Full name"
        value={claimant.name}
        onChange={(e) => setClaimant({ ...claimant, name: e.target.value })}
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Address line 1"
        value={claimant.address_line1}
        onChange={(e) =>
          setClaimant({ ...claimant, address_line1: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Town / city"
        value={claimant.town_city}
        onChange={(e) =>
          setClaimant({ ...claimant, town_city: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Postcode"
        value={claimant.postcode}
        onChange={(e) =>
          setClaimant({ ...claimant, postcode: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Email"
        value={claimant.email}
        onChange={(e) =>
          setClaimant({ ...claimant, email: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Phone"
        value={claimant.phone}
        onChange={(e) =>
          setClaimant({ ...claimant, phone: e.target.value })
        }
      />
    </div>,
    <div key="s2" className="space-y-4">
      <h2 className="text-xl font-semibold">About the respondent</h2>
      <input
        className="border rounded w-full p-2"
        placeholder="Full name"
        value={defendant.name}
        onChange={(e) => setDefendant({ ...defendant, name: e.target.value })}
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Address line 1"
        value={defendant.address_line1}
        onChange={(e) =>
          setDefendant({ ...defendant, address_line1: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Town / city"
        value={defendant.town_city}
        onChange={(e) =>
          setDefendant({ ...defendant, town_city: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Postcode"
        value={defendant.postcode}
        onChange={(e) =>
          setDefendant({ ...defendant, postcode: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Email"
        value={defendant.email}
        onChange={(e) =>
          setDefendant({ ...defendant, email: e.target.value })
        }
      />
      <input
        className="border rounded w-full p-2"
        placeholder="Phone"
        value={defendant.phone}
        onChange={(e) =>
          setDefendant({ ...defendant, phone: e.target.value })
        }
      />
    </div>,
    <div key="s3" className="space-y-4">
      <h2 className="text-xl font-semibold">About the claim</h2>
      <input
        className="border rounded w-full p-2"
        placeholder="One-line summary"
        value={claimInfo.dispute_summary_one_liner}
        onChange={(e) =>
          setClaimInfo({
            ...claimInfo,
            dispute_summary_one_liner: e.target.value
          })
        }
      />
      <input
        className="border rounded w-full p-2"
        type="number"
        placeholder="Amount claimed (GBP)"
        value={claimInfo.amount_claimed}
        onChange={(e) =>
          setClaimInfo({
            ...claimInfo,
            amount_claimed: Number(e.target.value)
          })
        }
      />
      <textarea
        className="border rounded w-full p-2"
        rows={5}
        placeholder="What happened? Give a clear timeline of events."
        value={claimInfo.facts_summary}
        onChange={(e) =>
          setClaimInfo({ ...claimInfo, facts_summary: e.target.value })
        }
      />
      <textarea
        className="border rounded w-full p-2"
        rows={3}
        placeholder="What do you want the court to order?"
        value={claimInfo.desired_outcome}
        onChange={(e) =>
          setClaimInfo({ ...claimInfo, desired_outcome: e.target.value })
        }
      />
      <textarea
        className="border rounded w-full p-2"
        rows={3}
        placeholder="What have you already done to try to resolve this?"
        value={claimInfo.pre_action_steps}
        onChange={(e) =>
          setClaimInfo({ ...claimInfo, pre_action_steps: e.target.value })
        }
      />

      <button
        type="button"
        onClick={handleSubmit}
        disabled={saving}
        className="px-4 py-2 bg-emerald-600 text-white rounded"
      >
        {saving ? "Saving..." : "Save & generate documents"}
      </button>

      {result && <p className="text-sm text-slate-700 mt-2">{result}</p>}
    </div>
  ];

  return <ClaimWizard steps={steps} />;
}
