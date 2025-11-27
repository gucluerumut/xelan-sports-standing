'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion, useScroll } from 'framer-motion';
import styles from './Navbar.module.css';

export default function Navbar() {
    const [isScrolled, setIsScrolled] = useState(false);
    const { scrollY } = useScroll();

    useEffect(() => {
        return scrollY.on('change', (latest) => {
            setIsScrolled(latest > 50);
        });
    }, [scrollY]);

    return (
        <motion.nav
            className={`${styles.navbar} ${isScrolled ? styles.scrolled : ''}`}
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div className={styles.container}>
                <Link href="/" className={styles.logo}>
                    <motion.span
                        className={styles.logoText}
                        whileHover={{ scale: 1.05 }}
                        transition={{ type: 'spring', stiffness: 300 }}
                    >
                        ⚽ Xelan Sports
                    </motion.span>
                </Link>

                <div className={styles.nav}>
                    {[
                        { href: '/', label: 'Home' },
                        { href: '/global', label: 'Global Rankings' },
                        { href: '/battle', label: 'Battle Mode' },
                    ].map((link) => (
                        <Link key={link.href} href={link.href} className={styles.navLink}>
                            <motion.span
                                whileHover={{ y: -2 }}
                                transition={{ duration: 0.2 }}
                            >
                                {link.label}
                            </motion.span>
                        </Link>
                    ))}
                </div>

                <div className={styles.actions}>
                    <motion.button
                        className={styles.searchBtn}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        🔍
                    </motion.button>
                </div>
            </div>
        </motion.nav>
    );
}
