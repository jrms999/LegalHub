import { ScotlandWizard } from "../../../components/ScotlandWizard";

export default function ScotlandClaimPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Simple Procedure – Scotland</h1>
      <p className="text-sm text-slate-700">
        This wizard helps you prepare a Simple Procedure claim summary, schedule of
        loss, and timeline. It does not file anything with the court and is not
        legal advice.
      </p>
      <ScotlandWizard />
    </div>
  );
}
