'use client';

import { useState } from 'react';
import Link from 'next/link';
import styles from './PillTabs.module.css';

interface Tab {
    name: string;
    slug: string;
    count?: number;
}

interface PillTabsProps {
    tabs: Tab[];
    activeTab?: string;
}

export default function PillTabs({ tabs, activeTab }: PillTabsProps) {
    const [active, setActive] = useState(activeTab || tabs[0]?.slug);

    return (
        <div className={styles.container}>
            {tabs.map((tab) => (
                <Link
                    key={tab.slug}
                    href={`/league/${tab.slug}`}
                    className={`${styles.tab} ${active === tab.slug ? styles.active : ''}`}
                    onClick={() => setActive(tab.slug)}
                >
                    {tab.name}
                    {tab.count && <span className={styles.count}>{tab.count}</span>}
                </Link>
            ))}
        </div>
    );
}
