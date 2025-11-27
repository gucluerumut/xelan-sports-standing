import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "Xelan Sports Standing - Digital Football Rankings",
  description: "Track football clubs' digital performance through social media metrics. League standings, global rankings, and head-to-head battles.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main style={{ paddingTop: '80px' }}>{children}</main>
      </body>
    </html>
  );
}
