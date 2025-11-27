'use client';

import Link from 'next/link';
import { useState } from 'react';
import styles from './ModernNav.module.css';

export default function ModernNav() {
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
                    <div className={styles.logoIcon}>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor" opacity="0.5" />
                            <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" />
                            <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" />
                        </svg>
                    </div>
                    <span className={styles.logoText}>StatsZone</span>
                </Link>

                <div className={styles.menu}>
                    <Link href="/" className={styles.menuItem}>
                        Ana Sayfa
                    </Link>

                    <div
                        className={styles.dropdown}
                        onMouseEnter={() => setIsLeaguesOpen(true)}
                        onMouseLeave={() => setIsLeaguesOpen(false)}
                    >
                        <button className={styles.menuItem}>
                            Ligler <span className={styles.arrow}>▾</span>
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
                        Oyuncular
                    </Link>

                    <Link href="/battle" className={styles.menuItem}>
                        Haberler
                    </Link>
                </div>

                <div className={styles.actions}>
                    <div className={styles.search}>
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                            <path d="M7 12C9.76142 12 12 9.76142 12 7C12 4.23858 9.76142 2 7 2C4.23858 2 2 4.23858 2 7C2 9.76142 4.23858 12 7 12Z" stroke="currentColor" strokeWidth="1.5" />
                            <path d="M11 11L14 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                        </svg>
                        <input
                            type="search"
                            placeholder="Oyuncu, takım ara..."
                            className={styles.searchInput}
                        />
                    </div>

                    <button className={styles.iconBtn}>
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M10 2C6.68629 2 4 4.68629 4 8C4 11.3137 6.68629 14 10 14C13.3137 14 16 11.3137 16 8C16 4.68629 13.3137 2 10 2Z" stroke="currentColor" strokeWidth="1.5" />
                            <path d="M10 14V18M7 18H13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                        </svg>
                    </button>

                    <div className={styles.avatar}>
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=user" alt="User" />
                    </div>
                </div>
            </div>
        </nav>
    );
}
