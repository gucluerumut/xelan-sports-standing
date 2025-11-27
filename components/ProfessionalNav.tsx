'use client';

import Link from 'next/link';
import { useState } from 'react';
import styles from './ProfessionalNav.module.css';

export default function ProfessionalNav() {
    const [isLeaguesOpen, setIsLeaguesOpen] = useState(false);

    const leagues = [
        { name: 'Premier League', slug: 'premier-league' },
        { name: 'La Liga', slug: 'la-liga' },
        { name: 'Süper Lig', slug: 'super-lig' },
        { name: 'Serie A', slug: 'serie-a' },
        { name: 'Bundesliga', slug: 'bundesliga' },
        { name: 'Ligue 1', slug: 'ligue-1' },
    ];

    return (
        <nav className={styles.nav}>
            <div className={styles.container}>
                <Link href="/" className={styles.logo}>
                    <span className={styles.logoIcon}>⚽</span>
                    <span className={styles.logoText}>XELAN SPORTS</span>
                </Link>

                <div className={styles.menu}>
                    <Link href="/" className={styles.menuItem}>
                        Home
                    </Link>

                    <div
                        className={styles.dropdown}
                        onMouseEnter={() => setIsLeaguesOpen(true)}
                        onMouseLeave={() => setIsLeaguesOpen(false)}
                    >
                        <button className={styles.menuItem}>
                            Leagues <span className={styles.arrow}>▾</span>
                        </button>
                        {isLeaguesOpen && (
                            <div className={styles.dropdownMenu}>
                                {leagues.map((league) => (
                                    <Link
                                        key={league.slug}
                                        href={`/league/${league.slug}`}
                                        className={styles.dropdownItem}
                                    >
                                        {league.name}
                                    </Link>
                                ))}
                            </div>
                        )}
                    </div>

                    <Link href="/global" className={styles.menuItem}>
                        Rankings
                    </Link>

                    <Link href="/battle" className={styles.menuItem}>
                        Compare
                    </Link>
                </div>

                <div className={styles.search}>
                    <input
                        type="search"
                        placeholder="Search clubs..."
                        className={styles.searchInput}
                    />
                </div>
            </div>
        </nav>
    );
}
