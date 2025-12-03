import { EnglandWalesWizard } from "../../../components/EnglandWalesWizard";

export default function EnglandWalesClaimPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Small claim – England &amp; Wales</h1>
      <p className="text-sm text-slate-700">
        This wizard helps you draft a Letter Before Claim and Particulars of Claim.
        It does not submit anything to the court and is not legal advice.
      </p>
      <EnglandWalesWizard />
    </div>
  );
}
