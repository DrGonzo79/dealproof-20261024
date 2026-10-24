import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DealProof — Stress-test a deal before the LOI",
  description: "Demo lender-realistic earnings bridge and DSCR stress test for small-business buyers."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
