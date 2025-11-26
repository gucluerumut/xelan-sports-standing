import React from 'react';
import { Instagram, Twitter } from 'lucide-react';
import { SiTiktok } from 'react-icons/si';

interface SocialMediaLinksProps {
    instagramUsername?: string;
    tiktokUsername?: string;
    twitterUsername?: string;
    size?: 'sm' | 'md' | 'lg';
    className?: string;
}

const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-10 h-10',
};

export function SocialMediaLinks({
    instagramUsername,
    tiktokUsername,
    twitterUsername,
    size = 'md',
    className = '',
}: SocialMediaLinksProps) {
    const iconSize = size === 'sm' ? 20 : size === 'md' ? 24 : 28;

    const socialLinks = [
        {
            platform: 'Instagram',
            username: instagramUsername,
            url: instagramUsername ? `https://instagram.com/${instagramUsername}` : null,
            icon: <Instagram size={iconSize} />,
            color: 'hover:text-pink-600',
            bgGradient: 'hover:from-purple-600 hover:via-pink-600 hover:to-orange-500',
        },
        {
            platform: 'TikTok',
            username: tiktokUsername,
            url: tiktokUsername ? `https://tiktok.com/@${tiktokUsername}` : null,
            icon: <SiTiktok size={iconSize} />,
            color: 'hover:text-black dark:hover:text-white',
            bgGradient: 'hover:from-black hover:to-cyan-500',
        },
        {
            platform: 'Twitter',
            username: twitterUsername,
            url: twitterUsername ? `https://twitter.com/${twitterUsername}` : null,
            icon: <Twitter size={iconSize} />,
            color: 'hover:text-blue-500',
            bgGradient: 'hover:from-blue-400 hover:to-blue-600',
        },
    ];

    const activeLinks = socialLinks.filter((link) => link.url);

    if (activeLinks.length === 0) {
        return null;
    }

    return (
        <div className={`flex items-center gap-3 ${className}`}>
            {activeLinks.map((link) => (
                <a
                    key={link.platform}
                    href={link.url!}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`
            ${sizeClasses[size]}
            flex items-center justify-center
            rounded-full
            bg-gray-100 dark:bg-gray-800
            text-gray-600 dark:text-gray-400
            ${link.color}
            transition-all duration-300
            hover:scale-110
            hover:shadow-lg
            group
          `}
                    title={`${link.platform}: @${link.username}`}
                    aria-label={`Visit ${link.platform} profile`}
                >
                    <div className="transition-transform duration-300 group-hover:scale-110">
                        {link.icon}
                    </div>
                </a>
            ))}
        </div>
    );
}
