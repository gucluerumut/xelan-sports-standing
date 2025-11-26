// Real Instagram data for Xelan Sports Standing
// Data sourced from Instagram profile scraper
import { Club } from './types';
import { CLUB_DATA } from './club-data-real';

// Export the real club data
export const MOCK_CLUBS: Club[] = CLUB_DATA;

export function calculateDigitalScore(metrics: Club['metrics']): number {
    const {
        instagramFollowers,
        instagramEngagement,
        tiktokFollowers,
        tiktokViews,
        twitterFollowers,
        twitterEngagement,
    } = metrics;

    // Weighted scoring formula
    const instagramScore = (instagramFollowers / 1000000) * 10 + instagramEngagement * 5;
    const tiktokScore = (tiktokFollowers / 1000000) * 8 + (tiktokViews / 100000000) * 6;
    const twitterScore = (twitterFollowers / 1000000) * 7 + twitterEngagement * 4;

    return Math.round(instagramScore + tiktokScore + twitterScore);
}

// Initialize digital scores
MOCK_CLUBS.forEach((club) => {
    club.digitalScore = calculateDigitalScore(club.metrics);
});

export function getClubsByLeague(leagueSlug: string): Club[] {
    const leagueMap: { [key: string]: string } = {
        'premier-league': 'Premier League',
        'la-liga': 'La Liga',
        'super-lig': 'Süper Lig',
        'serie-a': 'Serie A',
        'bundesliga': 'Bundesliga',
        'ligue-1': 'Ligue 1',
    };

    const leagueName = leagueMap[leagueSlug];
    return MOCK_CLUBS.filter((club) => club.league === leagueName).sort(
        (a, b) => b.digitalScore - a.digitalScore
    );
}

export function getGlobalStandings(): Club[] {
    return [...MOCK_CLUBS].sort((a, b) => b.digitalScore - a.digitalScore);
}

export function getClubById(id: string): Club | undefined {
    return MOCK_CLUBS.find((club) => club.id === id);
}
