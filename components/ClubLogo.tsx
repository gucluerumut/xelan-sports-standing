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

    // Strip common club suffixes before normalizing
    const baseName = clubName
        .replace(/ FC$/i, '')
        .replace(/ CF$/i, '')
        .replace(/ SK$/i, '')
        .replace(/ AS$/i, '')
        .replace(/ SC$/i, '')
        .replace(/ AC$/i, '')
        .replace(/ SS$/i, '')
        .replace(/ US$/i, '')
        .replace(/ RC$/i, '')
        .replace(/ RCD$/i, '')
        .replace(/ CD$/i, '')
        .replace(/ CA$/i, '')
        .replace(/ FK$/i, '')
        .replace(/ SV$/i, '')
        .replace(/ TSG$/i, '')
        .replace(/ VfL$/i, '')
        .replace(/ VfB$/i, '')
        .replace(/ 1\.$/i, '')
        .replace(/ \d{4}$/i, '') // Remove years like "1907"
        .trim();

    // Add local logo path as the first option
    const safeName = baseName.toLowerCase().replace(/ /g, '-').replace(/\./g, '').replace(/&/g, 'and').replace(/ç/g, 'c').replace(/ğ/g, 'g').replace(/ı/g, 'i').replace(/ö/g, 'o').replace(/ş/g, 's').replace(/ü/g, 'u');
    const localLogoPath = `/logos/${safeName}.png`;

    // Combine local path with remote URLs
    const allSources = [localLogoPath, ...logoUrls];

    const sizePx = size === 'sm' ? 36 : size === 'md' ? 48 : 64;
    const initials = getClubInitials(clubName);

    const handleError = () => {
        if (currentSrcIndex < allSources.length - 1) {
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

    if (hasError) {
        return (
            <div className={`${styles.logoPlaceholder} ${styles[size]} ${className}`}>
                <span className={styles.initials}>{initials}</span>
            </div>
        );
    }

    return (
        <div className={`${styles.logoWrapper} ${styles[size]} ${className}`}>
            <Image
                src={allSources[currentSrcIndex]}
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
