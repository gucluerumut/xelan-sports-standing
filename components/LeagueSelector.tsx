'use client';

import Link from 'next/link';
import { LEAGUES } from '@/lib/types';
import styles from './LeagueSelector.module.css';

interface LeagueSelectorProps {
    activeLeague?: string;
}

export default function LeagueSelector({ activeLeague }: LeagueSelectorProps) {
    return (
        <div className={styles.selector}>
            <h2 className={styles.title}>Select League</h2>
            <div className={styles.tabs}>
                {LEAGUES.map((league) => (
                    <Link
                        key={league.id}
                        href={`/league/${league.slug}`}
                        className={`${styles.tab} ${activeLeague === league.slug ? styles.active : ''}`}
                    >
                        <span className={styles.leagueName}>{league.name}</span>
                        <span className={styles.country}>{league.country}</span>
                    </Link>
                ))}
            </div>
        </div>
    );
}
