import Link from 'next/link';
import { LEAGUES } from '@/lib/types';
import { fetchLeagueStandings } from '@/lib/apify-service';
import LeagueSelector from '@/components/LeagueSelector';
import StandingsTable from '@/components/StandingsTable';
import styles from './page.module.css';

export default async function Home() {
  // Fetch top 5 clubs for each league
  const premierLeagueClubs = await fetchLeagueStandings('premier-league');
  const laLigaClubs = await fetchLeagueStandings('la-liga');
  const superLigClubs = await fetchLeagueStandings('super-lig');

  return (
    <div className="container">
      <section className={styles.hero}>
        <h1 className={styles.heroTitle}>
          Digital Football Rankings
        </h1>
        <p className={styles.heroSubtitle}>
          Track the social media power of football clubs across Instagram, TikTok, and Twitter
        </p>
      </section>

      <LeagueSelector />

      <section className={styles.leaguePreview}>
        <div className={styles.previewCard}>
          <div className={styles.previewHeader}>
            <h2>Premier League</h2>
            <Link href="/league/premier-league" className={styles.viewAll}>
              View All →
            </Link>
          </div>
          <StandingsTable
            clubs={premierLeagueClubs}
            title=""
            limit={5}
          />
        </div>

        <div className={styles.previewCard}>
          <div className={styles.previewHeader}>
            <h2>La Liga</h2>
            <Link href="/league/la-liga" className={styles.viewAll}>
              View All →
            </Link>
          </div>
          <StandingsTable
            clubs={laLigaClubs}
            title=""
            limit={5}
          />
        </div>

        <div className={styles.previewCard}>
          <div className={styles.previewHeader}>
            <h2>Süper Lig</h2>
            <Link href="/league/super-lig" className={styles.viewAll}>
              View All →
            </Link>
          </div>
          <StandingsTable
            clubs={superLigClubs}
            title=""
            limit={5}
          />
        </div>
      </section>

      <section className={styles.cta}>
        <h2>Explore More</h2>
        <div className={styles.ctaButtons}>
          <Link href="/global" className="btn btn-primary">
            Global Rankings
          </Link>
          <Link href="/battle" className="btn btn-secondary">
            Battle Mode
          </Link>
        </div>
      </section>
    </div>
  );
}
