'use client';

import { Club } from '@/lib/types';
import ClubCard from './ClubCard';
import styles from './StandingsTable.module.css';

interface StandingsTableProps {
    clubs: Club[];
    title: string;
    limit?: number;
}

export default function StandingsTable({ clubs, title, limit }: StandingsTableProps) {
    const displayClubs = limit ? clubs.slice(0, limit) : clubs;

    return (
        <div className={styles.container}>
            <h2 className={styles.title}>{title}</h2>
            <div className={styles.grid}>
                {displayClubs.map((club, index) => (
                    <div key={club.id} className={styles.cardWrapper}>
                        <ClubCard club={club} rank={index + 1} />
                    </div>
                ))}
            </div>
        </div>
    );
}
