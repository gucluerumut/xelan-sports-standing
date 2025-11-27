import type { Metadata } from "next";
import "./globals.css";
import ProfessionalNav from "@/components/ProfessionalNav";

export const metadata: Metadata = {
  title: "Xelan Sports - Digital Football Rankings",
  description: "Track football clubs' digital performance through social media metrics. League standings, global rankings, and head-to-head comparisons.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <ProfessionalNav />
        <main style={{ paddingTop: '60px', minHeight: 'calc(100vh - 60px)' }}>{children}</main>
      </body>
    </html>
  );
}
