'use client';

import { Club } from '@/lib/types';
import { SocialMediaLinks } from './SocialMediaLinks';
import styles from './ModernClubCard.module.css';

interface ModernClubCardProps {
    club: Club;
    rank: number;
}

export default function ModernClubCard({ club, rank }: ModernClubCardProps) {
    const formatNumber = (num: number): string => {
        if (num >= 1000000) {
            return `${(num / 1000000).toFixed(1)}M`;
        }
        if (num >= 1000) {
            return `${(num / 1000).toFixed(1)}K`;
        }
        return num.toString();
    };

    return (
        <div className={styles.card}>
            <div className={styles.header}>
                <div className={styles.rank}>#{rank}</div>
                <div className={styles.clubInfo}>
                    <div className={styles.logo}>
                        {club.name.substring(0, 2).toUpperCase()}
                    </div>
                    <div className={styles.details}>
                        <h3 className={styles.name}>{club.name}</h3>
                        <span className={styles.league}>{club.league}</span>
                    </div>
                </div>
                <div className={styles.score}>
                    <div className={styles.scoreValue}>{club.digitalScore.toLocaleString()}</div>
                    <div className={styles.scoreLabel}>Digital Score</div>
                </div>
            </div>

            <div className={styles.stats}>
                <div className={styles.statItem}>
                    <div className={styles.statIcon}>📷</div>
                    <div className={styles.statInfo}>
                        <div className={styles.statLabel}>Instagram</div>
                        <div className={styles.statValue}>{formatNumber(club.metrics.instagramFollowers)}</div>
                    </div>
                </div>
                <div className={styles.statItem}>
                    <div className={styles.statIcon}>🎵</div>
                    <div className={styles.statInfo}>
                        <div className={styles.statLabel}>TikTok</div>
                        <div className={styles.statValue}>{formatNumber(club.metrics.tiktokFollowers)}</div>
                    </div>
                </div>
                <div className={styles.statItem}>
                    <div className={styles.statIcon}>🐦</div>
                    <div className={styles.statInfo}>
                        <div className={styles.statLabel}>Twitter</div>
                        <div className={styles.statValue}>{formatNumber(club.metrics.twitterFollowers)}</div>
                    </div>
                </div>
            </div>

            <div className={styles.footer}>
                <SocialMediaLinks
                    instagramUsername={club.instagramUsername}
                    tiktokUsername={club.tiktokUsername}
                    twitterUsername={club.twitterUsername}
                    size="sm"
                />
                <button className={styles.viewBtn}>View Details →</button>
            </div>
        </div>
    );
}
