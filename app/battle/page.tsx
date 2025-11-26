'use client';

import { useState } from 'react';
import { fetchAllClubs } from '@/lib/apify-service';
import { Club } from '@/lib/types';
import BattleComparison from '@/components/BattleComparison';
import styles from './page.module.css';
import { use } from 'react';

export default function BattlePage() {
    const clubs = use(fetchAllClubs());
    const [club1Id, setClub1Id] = useState<string>('');
    const [club2Id, setClub2Id] = useState<string>('');

    const club1 = clubs.find((c) => c.id === club1Id);
    const club2 = clubs.find((c) => c.id === club2Id);

    const showComparison = club1 && club2 && club1Id !== club2Id;

    return (
        <div className="container">
            <section className={styles.header}>
                <h1 className={styles.title}>Battle Mode</h1>
                <p className={styles.subtitle}>
                    Compare the digital performance of two football clubs head-to-head
                </p>
            </section>

            <div className={styles.selectors}>
                <div className={styles.selectorGroup}>
                    <label htmlFor="club1" className={styles.label}>
                        Select First Club
                    </label>
                    <select
                        id="club1"
                        className={styles.select}
                        value={club1Id}
                        onChange={(e) => setClub1Id(e.target.value)}
                    >
                        <option value="">Choose a club...</option>
                        {clubs.map((club) => (
                            <option key={club.id} value={club.id}>
                                {club.name} ({club.league})
                            </option>
                        ))}
                    </select>
                </div>

                <div className={styles.vs}>VS</div>

                <div className={styles.selectorGroup}>
                    <label htmlFor="club2" className={styles.label}>
                        Select Second Club
                    </label>
                    <select
                        id="club2"
                        className={styles.select}
                        value={club2Id}
                        onChange={(e) => setClub2Id(e.target.value)}
                    >
                        <option value="">Choose a club...</option>
                        {clubs.map((club) => (
                            <option key={club.id} value={club.id}>
                                {club.name} ({club.league})
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            {showComparison && club1 && club2 && (
                <BattleComparison club1={club1} club2={club2} />
            )}

            {!showComparison && (club1Id || club2Id) && (
                <div className={styles.placeholder}>
                    <p>Select two different clubs to see the comparison</p>
                </div>
            )}
        </div>
    );
}
