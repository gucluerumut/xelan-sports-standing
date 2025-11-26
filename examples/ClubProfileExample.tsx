import { Club } from '@/lib/types';
import { SocialMediaLinks } from '@/components/SocialMediaLinks';

export default function ClubProfile({ club }: { club: Club }) {
    return (
        <div className="club-profile">
            {/* Club Header */}
            <div className="flex items-center gap-4 mb-6">
                <img
                    src={club.logo}
                    alt={club.name}
                    className="w-20 h-20"
                />
                <div>
                    <h1 className="text-3xl font-bold">{club.name}</h1>
                    <p className="text-gray-600">{club.league}</p>

                    {/* Social Media Links */}
                    <SocialMediaLinks
                        instagramUsername={club.instagramUsername}
                        tiktokUsername={club.tiktokUsername}
                        twitterUsername={club.twitterUsername}
                        size="md"
                        className="mt-3"
                    />
                </div>
            </div>

            {/* Club Metrics */}
            <div className="grid grid-cols-3 gap-4">
                <div className="stat-card">
                    <h3>Instagram</h3>
                    <p>{club.metrics.instagramFollowers.toLocaleString()}</p>
                </div>
                <div className="stat-card">
                    <h3>TikTok</h3>
                    <p>{club.metrics.tiktokFollowers.toLocaleString()}</p>
                </div>
                <div className="stat-card">
                    <h3>Twitter</h3>
                    <p>{club.metrics.twitterFollowers.toLocaleString()}</p>
                </div>
            </div>
        </div>
    );
}
