'use client';

import styles from './StatsCard.module.css';

interface StatsCardProps {
    value: string | number;
    label: string;
    icon?: string;
    trend?: string;
}

export default function StatsCard({ value, label, icon, trend }: StatsCardProps) {
    return (
        <div className={styles.card}>
            {icon && <div className={styles.icon}>{icon}</div>}
            <div className={styles.value}>{value}</div>
            <div className={styles.label}>{label}</div>
            {trend && <div className={styles.trend}>{trend}</div>}
        </div>
    );
}
