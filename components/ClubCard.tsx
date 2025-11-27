'use client';

import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { Club } from '@/lib/types';
import { SocialMediaLinks } from './SocialMediaLinks';
import styles from './ClubCard.module.css';

interface ClubCardProps {
    club: Club;
    rank: number;
}

export default function ClubCard({ club, rank }: ClubCardProps) {
    const [ref, inView] = useInView({
        triggerOnce: true,
        threshold: 0.1,
    });

    const formatNumber = (num: number): string => {
        if (num >= 1000000) {
            return `${(num / 1000000).toFixed(1)}M`;
        }
        if (num >= 1000) {
            return `${(num / 1000).toFixed(1)}K`;
        }
        return num.toString();
    };

    const cardVariants = {
        hidden: { opacity: 0, y: 50 },
        visible: { opacity: 1, y: 0 },
    };

    return (
        <motion.div
            ref={ref}
            className={styles.card}
            variants={cardVariants}
            initial="hidden"
            animate={inView ? 'visible' : 'hidden'}
            transition={{ duration: 0.5, ease: 'easeInOut' }}
            whileHover={{ y: -8 }}
        >
            <motion.div
                className={styles.rank}
                initial={{ scale: 0 }}
                animate={inView ? { scale: 1 } : { scale: 0 }}
                transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
            >
                <span className={styles.rankNumber}>#{rank}</span>
            </motion.div>

            <div className={styles.clubInfo}>
                <motion.div
                    className={styles.logoContainer}
                    whileHover={{ rotate: 360 }}
                    transition={{ duration: 0.6 }}
                >
                    <div className={styles.logoPlaceholder}>
                        {club.name.substring(0, 2).toUpperCase()}
                    </div>
                </motion.div>

                <div className={styles.details}>
                    <h3 className={styles.clubName}>{club.name}</h3>
                    <p className={styles.league}>{club.league}</p>
                    <SocialMediaLinks
                        instagramUsername={club.instagramUsername}
                        tiktokUsername={club.tiktokUsername}
                        twitterUsername={club.twitterUsername}
                        size="sm"
                        className="mt-2"
                    />
                </div>
            </div>

            <div className={styles.stats}>
                {[
                    { label: 'Instagram', value: club.metrics.instagramFollowers },
                    { label: 'TikTok', value: club.metrics.tiktokFollowers },
                    { label: 'Twitter', value: club.metrics.twitterFollowers },
                ].map((stat, index) => (
                    <motion.div
                        key={stat.label}
                        className={styles.statItem}
                        initial={{ opacity: 0, x: -20 }}
                        animate={inView ? { opacity: 1, x: 0 } : { opacity: 0, x: -20 }}
                        transition={{ delay: 0.3 + index * 0.1 }}
                    >
                        <span className={styles.statLabel}>{stat.label}</span>
                        <motion.span
                            className={styles.statValue}
                            initial={{ scale: 0 }}
                            animate={inView ? { scale: 1 } : { scale: 0 }}
                            transition={{ delay: 0.4 + index * 0.1, type: 'spring' }}
                        >
                            {formatNumber(stat.value)}
                        </motion.span>
                    </motion.div>
                ))}
            </div>

            <motion.div
                className={styles.score}
                initial={{ opacity: 0 }}
                animate={inView ? { opacity: 1 } : { opacity: 0 }}
                transition={{ delay: 0.6 }}
            >
                <span className={styles.scoreLabel}>Digital Score</span>
                <motion.span
                    className={styles.scoreValue}
                    initial={{ scale: 0 }}
                    animate={inView ? { scale: 1 } : { scale: 0 }}
                    transition={{ delay: 0.7, type: 'spring', stiffness: 150 }}
                >
                    {club.digitalScore.toLocaleString()}
                </motion.span>
            </motion.div>
        </motion.div>
    );
}
