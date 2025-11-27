'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import { getClubInitials } from '@/lib/club-logo-helper';
import styles from './ClubLogo.module.css';

interface ClubLogoProps {
    clubName: string;
    logoUrls: string[];
    size?: 'sm' | 'md' | 'lg';
    className?: string;
}

export default function ClubLogo({ clubName, logoUrls, size = 'md', className = '' }: ClubLogoProps) {
    const [currentSrcIndex, setCurrentSrcIndex] = useState(0);
    const [hasError, setHasError] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    const sizePx = size === 'sm' ? 36 : size === 'md' ? 48 : 64;
    const initials = getClubInitials(clubName);

    const handleError = () => {
        if (currentSrcIndex < logoUrls.length - 1) {
            // Try next source
            setCurrentSrcIndex(prev => prev + 1);
        } else {
            // All sources failed
            setHasError(true);
        }
    };

    const handleLoad = () => {
        setIsLoading(false);
    };

    // Reset state if clubName changes
    useEffect(() => {
        setCurrentSrcIndex(0);
        setHasError(false);
        setIsLoading(true);
    }, [clubName, logoUrls]);

    if (hasError || logoUrls.length === 0) {
        return (
            <div className={`${styles.logoPlaceholder} ${styles[size]} ${className}`}>
                <span className={styles.initials}>{initials}</span>
            </div>
        );
    }

    return (
        <div className={`${styles.logoWrapper} ${styles[size]} ${className}`}>
            <Image
                src={logoUrls[currentSrcIndex]}
                alt={`${clubName} logo`}
                width={sizePx}
                height={sizePx}
                className={`${styles.logoImage} ${isLoading ? styles.loading : ''}`}
                onError={handleError}
                onLoad={handleLoad}
                unoptimized // Allow external URLs without adding all domains to config
            />
        </div>
    );
}
