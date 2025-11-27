import { notFound } from 'next/navigation';
import Link from 'next/link';
import { fetchLeagueStandings } from '@/lib/apify-service';
import { LEAGUES } from '@/lib/types';
import DataTable from '@/components/DataTable';
import PillTabs from '@/components/PillTabs';
import StatsCard from '@/components/StatsCard';
import styles from './page.module.css';

interface PageProps {
    params: Promise<{
        slug: string;
    }>;
}

export async function generateStaticParams() {
    return LEAGUES.map((league) => ({
        slug: league.slug,
    }));
}

export default async function LeaguePage({ params }: PageProps) {
    const { slug } = await params;

    const league = LEAGUES.find((l) => l.slug === slug);

    if (!league) {
        notFound();
    }

    const clubs = await fetchLeagueStandings(slug);

    // Calculate league stats
    const totalFollowers = clubs.reduce((sum, club) =>
        sum + club.metrics.instagramFollowers + club.metrics.tiktokFollowers + club.metrics.twitterFollowers, 0
    );
    const avgScore = Math.round(clubs.reduce((sum, club) => sum + club.digitalScore, 0) / clubs.length);
    const topClub = clubs[0];

    // Prepare tabs for league selector
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
                    <span className={styles.breadcrumbCurrent}>{league.name}</span>
                </div>
                <h1 className={styles.title}>{league.name}</h1>
                <p className={styles.subtitle}>
                    {league.country} • Season 2025-26 • Digital Rankings
                </p>
            </section>

            {/* League Stats */}
            <section className={styles.stats}>
                <StatsCard
                    value={clubs.length.toString()}
                    label="Total Clubs"
                    icon="⚽"
                />
                <StatsCard
                    value={`${(totalFollowers / 1000000).toFixed(0)}M`}
                    label="Total Followers"
                    icon="👥"
                />
                <StatsCard
                    value={avgScore.toLocaleString()}
                    label="Avg Digital Score"
                    icon="📊"
                />
                <StatsCard
                    value={topClub?.name.substring(0, 15) || 'N/A'}
                    label="Top Club"
                    icon="🏆"
                />
            </section>

            {/* League Selector */}
            <section className={styles.section}>
                <h2 className={styles.sectionTitle}>All Leagues</h2>
                <PillTabs tabs={leagueTabs} activeTab={slug} />
            </section>

            {/* Standings Table */}
            <section className={styles.section}>
                <div className={styles.sectionHeader}>
                    <h2>League Standings</h2>
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
                    <p>See how clubs stack up against each other</p>
                </div>
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
