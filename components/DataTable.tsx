'use client';

import { Club } from '@/lib/types';
import { getClubLogoUrls } from '@/lib/club-logo-helper';
import ClubLogo from './ClubLogo';
import styles from './DataTable.module.css';

interface DataTableProps {
    clubs: Club[];
    showRank?: boolean;
    limit?: number;
}

export default function DataTable({ clubs, showRank = true, limit }: DataTableProps) {
    const displayClubs = limit ? clubs.slice(0, limit) : clubs;

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
        <div className={styles.tableWrapper}>
            <table className={styles.table}>
                <thead>
                    <tr>
                        {showRank && <th className={styles.rankCol}>Rank</th>}
                        <th className={styles.clubCol}>Club</th>
                        <th className={styles.leagueCol}>League</th>
                        <th className={styles.statCol}>Instagram</th>
                        <th className={styles.statCol}>TikTok</th>
                        <th className={styles.statCol}>Twitter</th>
                        <th className={styles.scoreCol}>Digital Score</th>
                        <th className={styles.actionCol}></th>
                    </tr>
                </thead>
                <tbody>
                    {displayClubs.map((club, index) => {
                        const logoUrls = getClubLogoUrls(club.name);

                        return (
                            <tr key={club.id} className={styles.row}>
                                {showRank && (
                                    <td className={styles.rankCell}>
                                        <span className={styles.rankNumber}>#{index + 1}</span>
                                    </td>
                                )}
                                <td className={styles.clubCell}>
                                    <div className={styles.clubInfo}>
                                        <div className={styles.clubLogo}>
                                            <ClubLogo
                                                clubName={club.name}
                                                logoUrls={logoUrls}
                                                size="sm"
                                            />
                                        </div>
                                        <span className={styles.clubName}>{club.name}</span>
                                    </div>
                                </td>
                                <td className={styles.leagueCell}>
                                    <span className={styles.leagueBadge}>{club.league}</span>
                                </td>
                                <td className={styles.statCell}>
                                    {formatNumber(club.metrics.instagramFollowers)}
                                </td>
                                <td className={styles.statCell}>
                                    {formatNumber(club.metrics.tiktokFollowers)}
                                </td>
                                <td className={styles.statCell}>
                                    {formatNumber(club.metrics.twitterFollowers)}
                                </td>
                                <td className={styles.scoreCell}>
                                    <span className={styles.score}>{club.digitalScore.toLocaleString()}</span>
                                </td>
                                <td className={styles.actionCell}>
                                    <button className={styles.viewBtn}>View →</button>
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
}
