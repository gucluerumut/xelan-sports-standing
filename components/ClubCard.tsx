'use client';

import Image from 'next/image';
import { Club } from '@/lib/types';
import { SocialMediaLinks } from './SocialMediaLinks';
import styles from './ClubCard.module.css';

interface ClubCardProps {
    club: Club;
    rank: number;
}

export default function ClubCard({ club, rank }: ClubCardProps) {
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
            <div className={styles.rank}>
                <span className={styles.rankNumber}>#{rank}</span>
            </div>

            <div className={styles.clubInfo}>
                <div className={styles.logoContainer}>
                    <div className={styles.logoPlaceholder}>
                        {club.name.substring(0, 2).toUpperCase()}
                    </div>
                </div>

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
                <div className={styles.statItem}>
                    <span className={styles.statLabel}>Instagram</span>
                    <span className={styles.statValue}>
                        {formatNumber(club.metrics.instagramFollowers)}
                    </span>
                </div>
                <div className={styles.statItem}>
                    <span className={styles.statLabel}>TikTok</span>
                    <span className={styles.statValue}>
                        {formatNumber(club.metrics.tiktokFollowers)}
                    </span>
                </div>
                <div className={styles.statItem}>
                    <span className={styles.statLabel}>Twitter</span>
                    <span className={styles.statValue}>
                        {formatNumber(club.metrics.twitterFollowers)}
                    </span>
                </div>
            </div>

            <div className={styles.score}>
                <span className={styles.scoreLabel}>Digital Score</span>
                <span className={styles.scoreValue}>{club.digitalScore.toLocaleString()}</span>
            </div>
        </div>
    );
}
