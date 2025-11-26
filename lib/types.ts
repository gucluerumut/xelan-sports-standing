// Type definitions for Xelan Sports Standing

export interface SocialMetrics {
  instagramFollowers: number;
  instagramEngagement: number;
  tiktokFollowers: number;
  tiktokViews: number;
  twitterFollowers: number;
  twitterEngagement: number;
}

export interface Club {
  id: string;
  name: string;
  logo: string;
  country: string;
  league: string;
  instagramUsername?: string;
  tiktokUsername?: string;
  twitterUsername?: string;
  metrics: SocialMetrics;
  digitalScore: number;
}

export interface League {
  id: string;
  name: string;
  country: string;
  slug: string;
}

export interface ApifyActorRun {
  id: string;
  status: string;
  defaultDatasetId: string;
}

export interface ApifyDatasetItem {
  username: string;
  followersCount?: number;
  engagement?: number;
  views?: number;
  [key: string]: any;
}

export const LEAGUES: League[] = [
  { id: 'pl', name: 'Premier League', country: 'England', slug: 'premier-league' },
  { id: 'll', name: 'La Liga', country: 'Spain', slug: 'la-liga' },
  { id: 'sl', name: 'Süper Lig', country: 'Turkey', slug: 'super-lig' },
  { id: 'sa', name: 'Serie A', country: 'Italy', slug: 'serie-a' },
  { id: 'bl', name: 'Bundesliga', country: 'Germany', slug: 'bundesliga' },
  { id: 'l1', name: 'Ligue 1', country: 'France', slug: 'ligue-1' },
];
