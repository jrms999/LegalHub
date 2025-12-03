import Link from "next/link";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">
        LawTech Claims Assistant
      </h1>
      <p>
        Guided wizard to help you prepare small claims in Scotland (Simple Procedure)
        and England & Wales (small claims / money claims).
      </p>
      <div className="grid gap-4 md:grid-cols-2">
        <Link
          href="/claims/new/scotland"
          className="border rounded-lg p-4 hover:bg-slate-100"
        >
          <h2 className="font-semibold">Start a Simple Procedure (Scotland)</h2>
          <p className="text-sm text-slate-600">
            Prepare a claim summary, schedule of loss, and timeline.
          </p>
        </Link>
        <Link
          href="/claims/new/england-wales"
          className="border rounded-lg p-4 hover:bg-slate-100"
        >
          <h2 className="font-semibold">Start a claim (England & Wales)</h2>
          <p className="text-sm text-slate-600">
            Draft a Letter Before Claim and Particulars of Claim.
          </p>
        </Link>
      </div>
    </div>
  );
}
