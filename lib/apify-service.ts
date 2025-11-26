// Apify service for fetching social media data
import { Club, ApifyActorRun, ApifyDatasetItem } from './types';
import { MOCK_CLUBS, calculateDigitalScore, getClubsByLeague, getGlobalStandings, getClubById } from './mock-data';

const APIFY_API_TOKEN = process.env.APIFY_API_TOKEN;
const USE_MOCK_DATA = !APIFY_API_TOKEN;

/**
 * Fetch club metrics from Apify or return mock data
 */
export async function fetchClubMetrics(clubId: string, platform: 'instagram' | 'tiktok' | 'twitter'): Promise<any> {
    if (USE_MOCK_DATA) {
        console.log('Using mock data (no Apify API token found)');
        return null; // Mock data is already populated
    }

    try {
        // Example Apify actor call structure (adjust actor IDs based on actual Apify actors)
        const actorIds: { [key: string]: string } = {
            instagram: 'apify/instagram-profile-scraper',
            tiktok: 'apify/tiktok-profile-scraper',
            twitter: 'apify/twitter-profile-scraper',
        };

        const actorId = actorIds[platform];
        const response = await fetch(`https://api.apify.com/v2/acts/${actorId}/runs`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${APIFY_API_TOKEN}`,
            },
            body: JSON.stringify({
                // Input parameters would go here based on the specific actor
                // This is a placeholder structure
            }),
        });

        if (!response.ok) {
            throw new Error(`Apify API error: ${response.statusText}`);
        }

        const run: ApifyActorRun = await response.json();

        // Wait for the run to complete and fetch results
        // This is simplified - in production you'd poll for completion
        const datasetResponse = await fetch(
            `https://api.apify.com/v2/datasets/${run.defaultDatasetId}/items`,
            {
                headers: {
                    Authorization: `Bearer ${APIFY_API_TOKEN}`,
                },
            }
        );

        const data: ApifyDatasetItem[] = await datasetResponse.json();
        return data;
    } catch (error) {
        console.error('Error fetching from Apify:', error);
        return null;
    }
}

/**
 * Get league standings (sorted by digital score)
 */
export async function fetchLeagueStandings(leagueSlug: string): Promise<Club[]> {
    if (USE_MOCK_DATA) {
        return getClubsByLeague(leagueSlug);
    }

    // In production, this would fetch data from Apify for all clubs in the league
    // For now, return mock data
    return getClubsByLeague(leagueSlug);
}

/**
 * Get global standings (all clubs across all leagues)
 */
export async function fetchGlobalStandings(): Promise<Club[]> {
    if (USE_MOCK_DATA) {
        return getGlobalStandings();
    }

    // In production, this would fetch data from Apify for all clubs
    return getGlobalStandings();
}

/**
 * Get a specific club by ID
 */
export async function fetchClubById(clubId: string): Promise<Club | undefined> {
    if (USE_MOCK_DATA) {
        return getClubById(clubId);
    }

    // In production, this would fetch data from Apify for the specific club
    return getClubById(clubId);
}

/**
 * Get all clubs for battle mode selection
 */
export async function fetchAllClubs(): Promise<Club[]> {
    if (USE_MOCK_DATA) {
        return MOCK_CLUBS;
    }

    // In production, this would fetch all clubs from Apify
    return MOCK_CLUBS;
}

export { calculateDigitalScore };
