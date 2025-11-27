import Link from 'next/link';
import { fetchLeagueStandings } from '@/lib/apify-service';
import { CLUB_DATA } from '@/lib/club-data-real';
import DataTable from '@/components/DataTable';
import StatsCard from '@/components/StatsCard';
import PillTabs from '@/components/PillTabs';
import ModernClubCard from '@/components/ModernClubCard';
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

  const leagues = [
    { name: 'Premier League', slug: 'premier-league' },
    { name: 'La Liga', slug: 'la-liga' },
    { name: 'Süper Lig', slug: 'super-lig' },
    { name: 'Serie A', slug: 'serie-a' },
    { name: 'Bundesliga', slug: 'bundesliga' },
    { name: 'Ligue 1', slug: 'ligue-1' },
  ];

  return (
    <div className="container">
      {/* Hero Section */}
      <section className={styles.hero}>
        <h1 className={styles.title}>Digital Football Rankings</h1>
        <p className={styles.subtitle}>
          Track the social media power of football clubs across Instagram, TikTok, and Twitter
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

      {/* League Selector */}
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Leagues</h2>
        <PillTabs tabs={leagues} activeTab="premier-league" />
      </section>

      {/* Top Clubs Table */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <h2>Top Clubs by Digital Score</h2>
          <Link href="/global" className="btn btn-ghost">
            View All Rankings →
          </Link>
        </div>
        <DataTable clubs={CLUB_DATA} limit={10} />
      </section>

      {/* Featured Clubs */}
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Featured Clubs</h2>
        <div className={styles.clubGrid}>
          {CLUB_DATA.slice(0, 6).map((club, index) => (
            <ModernClubCard key={club.id} club={club} rank={index + 1} />
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className={styles.cta}>
        <div className={styles.ctaContent}>
          <h2>Explore More</h2>
          <p>Discover detailed statistics and compare clubs across all leagues</p>
        </div>
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
