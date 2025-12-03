const API_BASE = "http://localhost:8000";

export async function createClaim(payload: any) {
  const res = await fetch(`${API_BASE}/claims`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(`Failed to create claim: ${res.statusText}`);
  }
  return res.json();
}

export async function generateDocuments(claimId: number) {
  const res = await fetch(`${API_BASE}/claims/${claimId}/generate`, {
    method: "POST"
  });
  if (!res.ok) {
    throw new Error(`Failed to generate docs: ${res.statusText}`);
  }
  return res.json();
}
