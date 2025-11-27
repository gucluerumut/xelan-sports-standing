'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Club } from '@/lib/types';
import styles from './SearchBar.module.css';

interface SearchBarProps {
    clubs: Club[];
    onSelect?: (club: Club) => void;
}

export default function SearchBar({ clubs, onSelect }: SearchBarProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<Club[]>([]);

    useEffect(() => {
        if (query.length > 0) {
            const filtered = clubs.filter((club) =>
                club.name.toLowerCase().includes(query.toLowerCase()) ||
                club.league.toLowerCase().includes(query.toLowerCase())
            ).slice(0, 5);
            setResults(filtered);
        } else {
            setResults([]);
        }
    }, [query, clubs]);

    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                setIsOpen(true);
            }
            if (e.key === 'Escape') {
                setIsOpen(false);
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, []);

    return (
        <>
            <motion.button
                className={styles.trigger}
                onClick={() => setIsOpen(true)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
            >
                <span className={styles.triggerIcon}>🔍</span>
                <span className={styles.triggerText}>Search clubs...</span>
                <span className={styles.triggerShortcut}>⌘K</span>
            </motion.button>

            <AnimatePresence>
                {isOpen && (
                    <>
                        <motion.div
                            className={styles.overlay}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsOpen(false)}
                        />
                        <motion.div
                            className={styles.modal}
                            initial={{ opacity: 0, scale: 0.95, y: -20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.95, y: -20 }}
                            transition={{ duration: 0.2 }}
                        >
                            <div className={styles.searchBox}>
                                <span className={styles.searchIcon}>🔍</span>
                                <input
                                    type="text"
                                    className={styles.input}
                                    placeholder="Search for a club..."
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    autoFocus
                                />
                            </div>

                            {results.length > 0 && (
                                <div className={styles.results}>
                                    {results.map((club, index) => (
                                        <motion.div
                                            key={club.id}
                                            className={styles.result}
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: index * 0.05 }}
                                            onClick={() => {
                                                onSelect?.(club);
                                                setIsOpen(false);
                                            }}
                                        >
                                            <div className={styles.resultLogo}>
                                                {club.name.substring(0, 2).toUpperCase()}
                                            </div>
                                            <div className={styles.resultInfo}>
                                                <div className={styles.resultName}>{club.name}</div>
                                                <div className={styles.resultLeague}>{club.league}</div>
                                            </div>
                                            <div className={styles.resultArrow}>→</div>
                                        </motion.div>
                                    ))}
                                </div>
                            )}

                            {query.length > 0 && results.length === 0 && (
                                <div className={styles.noResults}>
                                    No clubs found for "{query}"
                                </div>
                            )}
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </>
    );
}
