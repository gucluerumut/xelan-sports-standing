import type { Metadata } from "next";
import "./globals.css";
import ModernNav from "@/components/ModernNav";

export const metadata: Metadata = {
  title: "StatsZone - Digital Football Rankings",
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
        <ModernNav />
        <main style={{ paddingTop: '64px', minHeight: 'calc(100vh - 64px)' }}>{children}</main>
      </body>
    </html>
  );
}
