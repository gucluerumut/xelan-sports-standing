import Link from 'next/link';
import { fetchLeagueStandings } from '@/lib/apify-service';
import { CLUB_DATA } from '@/lib/club-data-real';
import DataTable from '@/components/DataTable';
import StatsCard from '@/components/StatsCard';
import styles from './page.module.css';

export default async function Home() {
  // Fetch top clubs for preview
  const premierLeagueClubs = await fetchLeagueStandings('premier-league');
  const laLigaClubs = await fetchLeagueStandings('la-liga');
  const superLigClubs = await fetchLeagueStandings('super-lig');

  // Calculate total followers
  const totalFollowers = CLUB_DATA.reduce((sum, club) =>
    sum + club.metrics.instagramFollowers + club.metrics.tiktokFollowers + club.metrics.twitterFollowers, 0
  );

  return (
    <div className="container">
      {/* Hero Section */}
      <section className={styles.hero}>
        <h1 className={styles.title}>Digital Football Rankings</h1>
        <p className={styles.subtitle}>
          Comprehensive social media performance tracker for football clubs across Instagram, TikTok, and Twitter
        </p>
      </section>

      {/* Quick Stats */}
      <section className={styles.stats}>
        <StatsCard value="113" label="Total Clubs" icon="⚽" />
        <StatsCard value="6" label="Leagues" icon="🏆" />
        <StatsCard
          value={`${(totalFollowers / 1000000000).toFixed(1)}B`}
          label="Total Followers"
          icon="👥"
        />
        <StatsCard value="Live" label="Updates" icon="📊" />
      </section>

      {/* Top Clubs */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <h2>Top Clubs by Digital Score</h2>
          <Link href="/global" className="btn btn-ghost">
            View All Rankings →
          </Link>
        </div>
        <DataTable clubs={CLUB_DATA} limit={10} />
      </section>

      {/* League Previews */}
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Leagues</h2>
        <div className={styles.leagueGrid}>
          <div className={styles.leagueCard}>
            <div className={styles.leagueHeader}>
              <h3>Premier League</h3>
              <Link href="/league/premier-league" className="btn btn-secondary btn-sm">
                View All →
              </Link>
            </div>
            <DataTable clubs={premierLeagueClubs} limit={5} showRank={false} />
          </div>

          <div className={styles.leagueCard}>
            <div className={styles.leagueHeader}>
              <h3>La Liga</h3>
              <Link href="/league/la-liga" className="btn btn-secondary btn-sm">
                View All →
              </Link>
            </div>
            <DataTable clubs={laLigaClubs} limit={5} showRank={false} />
          </div>

          <div className={styles.leagueCard}>
            <div className={styles.leagueHeader}>
              <h3>Süper Lig</h3>
              <Link href="/league/super-lig" className="btn btn-secondary btn-sm">
                View All →
              </Link>
            </div>
            <DataTable clubs={superLigClubs} limit={5} showRank={false} />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className={styles.cta}>
        <h2>Explore More</h2>
        <div className={styles.ctaButtons}>
          <Link href="/global" className="btn btn-primary">
            Global Rankings
          </Link>
          <Link href="/battle" className="btn btn-secondary">
            Compare Clubs
          </Link>
        </div>
      </section>
    </div>
  );
}
