import { notFound } from 'next/navigation';
import { fetchLeagueStandings } from '@/lib/apify-service';
import { LEAGUES } from '@/lib/types';
import LeagueSelector from '@/components/LeagueSelector';
import StandingsTable from '@/components/StandingsTable';
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

    return (
        <div className="container">
            <section className={styles.header}>
                <h1 className={styles.title}>{league.name}</h1>
                <p className={styles.subtitle}>
                    {league.country} • Season 2025-26 • Digital Rankings
                </p>
            </section>

            <LeagueSelector activeLeague={slug} />

            <StandingsTable
                clubs={clubs}
                title={`Top ${clubs.length} Clubs`}
            />
        </div>
    );
}
