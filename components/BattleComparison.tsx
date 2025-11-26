'use client';

import { Club } from '@/lib/types';
import styles from './BattleComparison.module.css';

interface BattleComparisonProps {
    club1: Club;
    club2: Club;
}

export default function BattleComparison({ club1, club2 }: BattleComparisonProps) {
    const calculatePercentage = (value1: number, value2: number): number => {
        const total = value1 + value2;
        return total > 0 ? (value1 / total) * 100 : 50;
    };

    const formatNumber = (num: number): string => {
        if (num >= 1000000) {
            return `${(num / 1000000).toFixed(1)}M`;
        }
        if (num >= 1000) {
            return `${(num / 1000).toFixed(1)}K`;
        }
        return num.toString();
    };

    const metrics = [
        {
            label: 'Instagram Followers',
            value1: club1.metrics.instagramFollowers,
            value2: club2.metrics.instagramFollowers,
        },
        {
            label: 'Instagram Engagement',
            value1: club1.metrics.instagramEngagement,
            value2: club2.metrics.instagramEngagement,
        },
        {
            label: 'TikTok Followers',
            value1: club1.metrics.tiktokFollowers,
            value2: club2.metrics.tiktokFollowers,
        },
        {
            label: 'TikTok Views',
            value1: club1.metrics.tiktokViews,
            value2: club2.metrics.tiktokViews,
        },
        {
            label: 'Twitter Followers',
            value1: club1.metrics.twitterFollowers,
            value2: club2.metrics.twitterFollowers,
        },
        {
            label: 'Twitter Engagement',
            value1: club1.metrics.twitterEngagement,
            value2: club2.metrics.twitterEngagement,
        },
    ];

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <div className={styles.clubHeader}>
                    <div className={styles.logoPlaceholder}>
                        {club1.name.substring(0, 2).toUpperCase()}
                    </div>
                    <div>
                        <h3 className={styles.clubName}>{club1.name}</h3>
                        <p className={styles.league}>{club1.league}</p>
                    </div>
                </div>

                <div className={styles.vs}>VS</div>

                <div className={styles.clubHeader}>
                    <div className={styles.logoPlaceholder}>
                        {club2.name.substring(0, 2).toUpperCase()}
                    </div>
                    <div>
                        <h3 className={styles.clubName}>{club2.name}</h3>
                        <p className={styles.league}>{club2.league}</p>
                    </div>
                </div>
            </div>

            <div className={styles.scoreComparison}>
                <div className={styles.scoreBox}>
                    <span className={styles.scoreLabel}>Digital Score</span>
                    <span className={styles.scoreValue}>{club1.digitalScore.toLocaleString()}</span>
                </div>
                <div className={styles.scoreBox}>
                    <span className={styles.scoreLabel}>Digital Score</span>
                    <span className={styles.scoreValue}>{club2.digitalScore.toLocaleString()}</span>
                </div>
            </div>

            <div className={styles.metrics}>
                {metrics.map((metric, index) => {
                    const percentage1 = calculatePercentage(metric.value1, metric.value2);
                    const percentage2 = 100 - percentage1;

                    return (
                        <div key={index} className={styles.metricRow}>
                            <div className={styles.metricLabel}>{metric.label}</div>

                            <div className={styles.barContainer}>
                                <span className={styles.value}>{formatNumber(metric.value1)}</span>
                                <div className={styles.bar}>
                                    <div
                                        className={styles.barFill1}
                                        style={{ width: `${percentage1}%` }}
                                    />
                                    <div
                                        className={styles.barFill2}
                                        style={{ width: `${percentage2}%` }}
                                    />
                                </div>
                                <span className={styles.value}>{formatNumber(metric.value2)}</span>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
