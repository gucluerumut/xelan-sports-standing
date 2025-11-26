'use client';

import Link from 'next/link';
import { LEAGUES } from '@/lib/types';
import styles from './Header.module.css';

export default function Header() {
    return (
        <header className={styles.header}>
            <div className="container">
                <div className={styles.headerContent}>
                    <Link href="/" className={styles.logo}>
                        <h1 className={styles.logoText}>Xelan Sports Standing</h1>
                        <span className={styles.season}>Season 2025-26</span>
                    </Link>

                    <nav className={styles.nav}>
                        <Link href="/" className={styles.navLink}>Home</Link>
                        <Link href="/global" className={styles.navLink}>Global</Link>
                        <Link href="/battle" className={styles.navLink}>Battle</Link>
                    </nav>
                </div>
            </div>
        </header>
    );
}
