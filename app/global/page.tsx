import { fetchGlobalStandings } from '@/lib/apify-service';
import StandingsTable from '@/components/StandingsTable';
import styles from './page.module.css';

export default async function GlobalPage() {
    const clubs = await fetchGlobalStandings();

    return (
        <div className="container">
            <section className={styles.header}>
                <h1 className={styles.title}>Global Digital Rankings</h1>
                <p className={styles.subtitle}>
                    All clubs across all leagues ranked by digital performance
                </p>
            </section>

            <div className={styles.stats}>
                <div className={styles.statCard}>
                    <span className={styles.statValue}>{clubs.length}</span>
                    <span className={styles.statLabel}>Total Clubs</span>
                </div>
                <div className={styles.statCard}>
                    <span className={styles.statValue}>3</span>
                    <span className={styles.statLabel}>Leagues</span>
                </div>
                <div className={styles.statCard}>
                    <span className={styles.statValue}>2025-26</span>
                    <span className={styles.statLabel}>Season</span>
                </div>
            </div>

            <StandingsTable
                clubs={clubs}
                title="Top 20 Clubs Worldwide"
                limit={20}
            />
        </div>
    );
}
