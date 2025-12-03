import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LawTech Claims Assistant",
  description: "Guided small claims / simple procedure assistant"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900">
        <main className="max-w-4xl mx-auto py-8 px-4">{children}</main>
      </body>
    </html>
  );
}
