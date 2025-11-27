'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { CLUB_DATA } from '@/lib/club-data-real';
import { fetchLeagueStandings } from '@/lib/apify-service';
import LeagueSelector from '@/components/LeagueSelector';
import StandingsTable from '@/components/StandingsTable';
import SearchBar from '@/components/SearchBar';
import styles from './page.module.css';

export default async function Home() {
  // Fetch top 5 clubs for each league
  const premierLeagueClubs = await fetchLeagueStandings('premier-league');
  const laLigaClubs = await fetchLeagueStandings('la-liga');
  const superLigClubs = await fetchLeagueStandings('super-lig');

  return (
    <div className="container">
      {/* Enhanced Hero Section */}
      <motion.section
        className={styles.hero}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        <motion.h1
          className={styles.heroTitle}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          Digital Football Rankings
        </motion.h1>
        <motion.p
          className={styles.heroSubtitle}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          Track the social media power of football clubs across Instagram, TikTok, and Twitter
        </motion.p>

        {/* Search Bar */}
        <motion.div
          className={styles.searchContainer}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          <SearchBar clubs={CLUB_DATA} />
        </motion.div>
      </motion.section>

      <LeagueSelector />

      {/* League Previews */}
      <section className={styles.leaguePreview}>
        {[
          { title: 'Premier League', clubs: premierLeagueClubs, slug: 'premier-league' },
          { title: 'La Liga', clubs: laLigaClubs, slug: 'la-liga' },
          { title: 'Süper Lig', clubs: superLigClubs, slug: 'super-lig' },
        ].map((league, index) => (
          <motion.div
            key={league.slug}
            className={styles.previewCard}
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 0.6, delay: index * 0.1 }}
          >
            <div className={styles.previewHeader}>
              <h2>{league.title}</h2>
              <Link href={`/league/${league.slug}`} className={styles.viewAll}>
                View All →
              </Link>
            </div>
            <StandingsTable
              clubs={league.clubs}
              title=""
              limit={5}
            />
          </motion.div>
        ))}
      </section>

      {/* CTA Section */}
      <motion.section
        className={styles.cta}
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        <h2>Explore More</h2>
        <div className={styles.ctaButtons}>
          <Link href="/global" className="btn btn-primary">
            Global Rankings
          </Link>
          <Link href="/battle" className="btn btn-secondary">
            Battle Mode
          </Link>
        </div>
      </motion.section>
    </div>
  );
}
