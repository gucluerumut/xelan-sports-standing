'use client';

import styles from './LoadingSkeleton.module.css';

interface LoadingSkeletonProps {
    type?: 'card' | 'hero' | 'table';
    count?: number;
}

export default function LoadingSkeleton({ type = 'card', count = 1 }: LoadingSkeletonProps) {
    if (type === 'hero') {
        return (
            <div className={styles.heroSkeleton}>
                <div className={`${styles.skeleton} ${styles.title}`}></div>
                <div className={`${styles.skeleton} ${styles.subtitle}`}></div>
            </div>
        );
    }

    if (type === 'table') {
        return (
            <div className={styles.tableSkeleton}>
                {Array.from({ length: count }).map((_, i) => (
                    <div key={i} className={styles.rowSkeleton}>
                        <div className={`${styles.skeleton} ${styles.rank}`}></div>
                        <div className={`${styles.skeleton} ${styles.logo}`}></div>
                        <div className={styles.info}>
                            <div className={`${styles.skeleton} ${styles.name}`}></div>
                            <div className={`${styles.skeleton} ${styles.league}`}></div>
                        </div>
                        <div className={styles.stats}>
                            <div className={`${styles.skeleton} ${styles.stat}`}></div>
                            <div className={`${styles.skeleton} ${styles.stat}`}></div>
                            <div className={`${styles.skeleton} ${styles.stat}`}></div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    // Default: card skeleton
    return (
        <div className={styles.cardGrid}>
            {Array.from({ length: count }).map((_, i) => (
                <div key={i} className={styles.cardSkeleton}>
                    <div className={styles.cardHeader}>
                        <div className={`${styles.skeleton} ${styles.logo}`}></div>
                        <div className={styles.cardInfo}>
                            <div className={`${styles.skeleton} ${styles.name}`}></div>
                            <div className={`${styles.skeleton} ${styles.league}`}></div>
                        </div>
                        <div className={`${styles.skeleton} ${styles.rank}`}></div>
                    </div>
                    <div className={styles.cardStats}>
                        <div className={`${styles.skeleton} ${styles.stat}`}></div>
                        <div className={`${styles.skeleton} ${styles.stat}`}></div>
                        <div className={`${styles.skeleton} ${styles.stat}`}></div>
                    </div>
                    <div className={`${styles.skeleton} ${styles.score}`}></div>
                </div>
            ))}
        </div>
    );
}
