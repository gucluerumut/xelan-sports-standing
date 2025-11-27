import Link from 'next/link';
import { fetchGlobalStandings } from '@/lib/apify-service';
import { CLUB_DATA } from '@/lib/club-data-real';
import DataTable from '@/components/DataTable';
import StatsCard from '@/components/StatsCard';
import PillTabs from '@/components/PillTabs';
import { LEAGUES } from '@/lib/types';
import styles from './page.module.css';

export default async function GlobalPage() {
    const clubs = await fetchGlobalStandings();

    // Calculate global stats
    const totalFollowers = CLUB_DATA.reduce((sum, club) =>
        sum + club.metrics.instagramFollowers + club.metrics.tiktokFollowers + club.metrics.twitterFollowers, 0
    );
    const avgScore = Math.round(CLUB_DATA.reduce((sum, club) => sum + club.digitalScore, 0) / CLUB_DATA.length);
    const topClub = clubs[0];

    // Prepare league tabs
    const leagueTabs = LEAGUES.map(l => ({
        name: l.name,
        slug: l.slug,
        count: undefined
    }));

    return (
        <div className="container">
            {/* Hero Section */}
            <section className={styles.hero}>
                <div className={styles.breadcrumb}>
                    <Link href="/" className={styles.breadcrumbLink}>Home</Link>
                    <span className={styles.breadcrumbSeparator}>/</span>
                    <span className={styles.breadcrumbCurrent}>Global Rankings</span>
                </div>
                <h1 className={styles.title}>Global Digital Rankings</h1>
                <p className={styles.subtitle}>
                    All clubs across all leagues ranked by digital performance
                </p>
            </section>

            {/* Global Stats */}
            <section className={styles.stats}>
                <StatsCard
                    value={CLUB_DATA.length.toString()}
                    label="Total Clubs"
                    icon="⚽"
                />
                <StatsCard
                    value="6"
                    label="Leagues"
                    icon="🏆"
                />
                <StatsCard
                    value={`${(totalFollowers / 1000000000).toFixed(1)}B`}
                    label="Total Followers"
                    icon="👥"
                />
                <StatsCard
                    value={topClub?.name.substring(0, 12) || 'N/A'}
                    label="Top Club"
                    icon="🥇"
                />
            </section>

            {/* League Filter */}
            <section className={styles.section}>
                <h2 className={styles.sectionTitle}>Filter by League</h2>
                <PillTabs tabs={leagueTabs} />
            </section>

            {/* Global Rankings Table */}
            <section className={styles.section}>
                <div className={styles.sectionHeader}>
                    <h2>Top Clubs Worldwide</h2>
                    <div className={styles.tableInfo}>
                        <span className={styles.tableCount}>{clubs.length} clubs</span>
                    </div>
                </div>
                <DataTable clubs={clubs} showRank={true} />
            </section>

            {/* CTA */}
            <section className={styles.cta}>
                <div className={styles.ctaContent}>
                    <h2>Compare Clubs</h2>
                    <p>See detailed comparisons between your favorite clubs</p>
                </div>
                <div className={styles.ctaButtons}>
                    <Link href="/battle" className="btn btn-primary">
                        Battle Mode
                    </Link>
                    <Link href="/" className="btn btn-secondary">
                        Back to Home
                    </Link>
                </div>
            </section>
        </div>
    );
}
