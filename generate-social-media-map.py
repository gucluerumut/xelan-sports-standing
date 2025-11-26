#!/usr/bin/env python3
"""
Add TikTok and Twitter usernames to all clubs in club-data-real.ts
"""

import json
import re

# Load TikTok data
with open('tiktok-follower-data.json', 'r') as f:
    tiktok_data = json.load(f)

# Load Twitter handles
with open('twitter-scraper-input.json', 'r') as f:
    twitter_data = json.load(f)

# Create mappings
tiktok_map = {}
for profile in tiktok_data.get('data', []):
    username = profile.get('username') or profile.get('unique_id')
    if username:
        tiktok_map[username.lower()] = username

twitter_handles = twitter_data.get('twitterHandles', [])

# Manual mapping for clubs (Instagram username -> TikTok/Twitter)
# This maps Instagram usernames to their TikTok and Twitter equivalents
SOCIAL_MEDIA_MAP = {
    # Premier League (already done for first 6)
    'nufc': {'tiktok': 'nufc', 'twitter': 'NUFC'},
    'avfcofficial': {'tiktok': 'avfcofficial', 'twitter': 'AVFCOfficial'},
    'officialbhafc': {'tiktok': 'officialbhafc', 'twitter': 'OfficialBHAFC'},
    'wolves': {'tiktok': 'wolves', 'twitter': 'Wolves'},
    'westham': {'tiktok': 'westham', 'twitter': 'WestHam'},
    'cpfc': {'tiktok': 'cpfc', 'twitter': 'CPFC'},
    'fulhamfc': {'tiktok': 'fulhamfc', 'twitter': 'FulhamFC'},
    'everton': {'tiktok': 'everton', 'twitter': 'Everton'},
    'brentfordfc': {'tiktok': 'brentfordfc', 'twitter': 'BrentfordFC'},
    'nffc': {'tiktok': None, 'twitter': 'NFFC'},  # No TikTok
    'afcbournemouth': {'tiktok': 'afcbournemouth', 'twitter': 'afcbournemouth'},
    'leedsunited': {'tiktok': 'leedsunited', 'twitter': 'LUFC'},
    'burnleyofficial': {'tiktok': 'burnleyofficial', 'twitter': 'BurnleyOfficial'},
    'sunderlandafc': {'tiktok': 'sunderlandafc', 'twitter': 'SunderlandAFC'},
    
    # La Liga
    'realmadrid': {'tiktok': 'realmadrid', 'twitter': 'realmadrid'},
    'fcbarcelona': {'tiktok': 'fcbarcelona', 'twitter': 'FCBarcelona'},
    'atleticodemadrid': {'tiktok': 'atleticodemadrid', 'twitter': 'Atleti'},
    'realbe': {'tiktok': 'realbetisbalompie', 'twitter': 'RealBetis'},
    'valenciacf': {'tiktok': 'valenciacf', 'twitter': 'valenciacf'},
    'sevillafc': {'tiktok': 'sevillafc', 'twitter': 'SevillaFC'},
    'athletic_club': {'tiktok': 'athleticclub', 'twitter': 'AthleticClub'},
    'realsociedad': {'tiktok': 'realsociedad', 'twitter': 'RealSociedad'},
    'villarrealcf': {'tiktok': 'villarrealcf', 'twitter': 'VillarrealCF'},
    'rayovallecano': {'tiktok': 'rayovallecano', 'twitter': 'RayoVallecano'},
    'getafecf': {'tiktok': 'getafecf', 'twitter': 'GetafeCF'},
    'gironafc': {'tiktok': 'gironafc', 'twitter': 'GironaFC'},
    'rcdmallorca': {'tiktok': None, 'twitter': 'RCD_Mallorca'},  # No TikTok
    'deportivoalaves': {'tiktok': 'deportivoalaves', 'twitter': 'Alaves'},
    'rcdesp': {'tiktok': 'rcdesp', 'twitter': 'RCDEspanyol'},
    'rccelta': {'tiktok': 'rccelta', 'twitter': 'RCCelta'},
    'caosasuna': {'tiktok': 'caosasuna', 'twitter': 'CAOsasuna'},
    'elchecf': {'tiktok': 'elchecf', 'twitter': 'Elchecf_en'},
    'levanteud': {'tiktok': 'levanteud', 'twitter': 'LevanteUD'},
    'realoviedosad': {'tiktok': 'realoviedosad', 'twitter': 'RealOviedo'},
    
    # Süper Lig
    'galatasaray': {'tiktok': 'galatasaray', 'twitter': 'GalatasaraySK'},
    'fenerbahce': {'tiktok': 'fenerbahce', 'twitter': 'Fenerbahce'},
    'besiktas': {'tiktok': None, 'twitter': 'Besiktas'},  # No official TikTok
    'trabzonspor': {'tiktok': 'trabzonspor', 'twitter': 'Trabzonspor'},
    'basaksehirfk': {'tiktok': 'ibfk2014', 'twitter': 'ibfk2014'},
    'samsunsporkulubu': {'tiktok': 'samsunsporkulubu', 'twitter': 'SamsunSporKul'},
    'goztepe': {'tiktok': None, 'twitter': 'Goztepe'},
    'konyaspor': {'tiktok': 'konyaspor', 'twitter': 'konyaspor'},
    'alanyaspor': {'tiktok': None, 'twitter': 'Alanyaspor'},
    'antalyaspor': {'tiktok': None, 'twitter': 'Antalyaspor'},
    'gaziantepfk': {'tiktok': None, 'twitter': 'GaziantepFK'},
    'kasimpasask': {'tiktok': None, 'twitter': 'KasimpasaSK'},
    'kayserispor': {'tiktok': None, 'twitter': 'Kayserispor'},
    'eyupspor': {'tiktok': None, 'twitter': 'Eyupspor'},
    'rizespor': {'tiktok': None, 'twitter': 'Rizespor'},
    'fatihkaragumruk': {'tiktok': None, 'twitter': 'fkaragumruk'},
    'genclerbirligi': {'tiktok': None, 'twitter': 'Genclerbirligi'},
    'kocaelispor': {'tiktok': None, 'twitter': 'Kocaelispor'},
    
    # Serie A
    'juventus': {'tiktok': 'juventus', 'twitter': 'juventusfc'},
    'acmilan': {'tiktok': 'acmilan', 'twitter': 'acmilan'},
    'inter': {'tiktok': 'inter', 'twitter': 'Inter'},
    'sscnapoli': {'tiktok': 'sscnapoli', 'twitter': 'sscnapoli'},
    'asroma': {'tiktok': 'asroma', 'twitter': 'OfficialASRoma'},
    'acffiorentina': {'tiktok': 'acffiorentina', 'twitter': 'acffiorentina'},
    'sslazio': {'tiktok': None, 'twitter': 'OfficialSSLazio'},
    'atalantabc': {'tiktok': None, 'twitter': 'Atalanta_BC'},
    'como1907': {'tiktok': None, 'twitter': 'Como_1907'},
    'parmacalcio1913': {'tiktok': 'parmacalcio1913', 'twitter': '1913parmacalcio'},
    'bolognafc1909': {'tiktok': None, 'twitter': 'BfcOfficialPage'},
    'cagliaricalcio': {'tiktok': 'cagliaricalcio', 'twitter': 'CagliariCalcio'},
    'torinofc_1906': {'tiktok': 'torinofc_1906', 'twitter': 'TorinoFC_1906'},
    'genoac': {'tiktok': 'genoac', 'twitter': 'GenoaCFC'},
    'udinese_1896': {'tiktok': 'udinese_1896', 'twitter': 'Udinese_1896'},
    'hellasveronaf': {'tiktok': 'hellasveronaf', 'twitter': 'HellasVeronaFC'},
    'uslecce': {'tiktok': 'uslecce', 'twitter': 'OfficialUSLecce'},
    'sassuolous': {'tiktok': 'sassuolous', 'twitter': 'SassuoloUS'},
    'pisasportingclub': {'tiktok': 'pisasportingclub', 'twitter': 'PisaSC'},
    'uscremonese': {'tiktok': 'uscremonese', 'twitter': 'USCremonese'},
    
    # Bundesliga
    'fcbayern': {'tiktok': 'fcbayern', 'twitter': 'FCBayern'},
    'bvb09': {'tiktok': 'bvb', 'twitter': 'BVB'},
    'bayer04fussball': {'tiktok': 'bayer04', 'twitter': 'bayer04fussball'},
    'dierotenbullen': {'tiktok': 'dierotenbullen', 'twitter': 'RBLeipzig'},
    'eintracht': {'tiktok': 'eintracht', 'twitter': 'Eintracht'},
    'borussia': {'tiktok': 'borussia', 'twitter': 'borussia'},
    'vfl_wolfsburg': {'tiktok': 'vfl_wolfsburg', 'twitter': 'VfL_Wolfsburg'},
    'vfb': {'tiktok': 'vfb', 'twitter': 'VfB'},
    'scfreiburg': {'tiktok': 'scfreiburg', 'twitter': 'scfreiburg'},
    'werderbremen': {'tiktok': 'werderbremen', 'twitter': 'werderbremen'},
    'tsg_1899_hoffenheim': {'tiktok': 'tsg_1899_hoffenheim', 'twitter': 'achtzehn99'},
    'fcstpauli': {'tiktok': 'fcstpauli', 'twitter': 'fcstpauli'},
    '1fsv_mainz_05': {'tiktok': '1fsv_mainz_05', 'twitter': 'Mainz05'},
    'fcaugsburg': {'tiktok': 'fcaugsburg', 'twitter': 'FCAugsburg'},
    '1_fc_union_berlin': {'tiktok': None, 'twitter': 'fcunion'},
    '1_fc_heidenheim': {'tiktok': None, 'twitter': 'FCH1846'},
    'hsv': {'tiktok': None, 'twitter': 'HSV'},
    'effzeh': {'tiktok': 'effzeh', 'twitter': 'fckoeln'},
    
    # Ligue 1
    'psg': {'tiktok': 'psg', 'twitter': 'PSG_inside'},
    'olympiquedemarseille': {'tiktok': 'om', 'twitter': 'OM_Officiel'},
    'asmonaco': {'tiktok': 'asmonaco', 'twitter': 'AS_Monaco'},
    'ol': {'tiktok': None, 'twitter': 'OL'},
    'losc': {'tiktok': 'losc', 'twitter': 'losclive'},
    'ogcnice': {'tiktok': 'ogcnice', 'twitter': 'ogcnice'},
    'fcnantes': {'tiktok': 'fcnantes', 'twitter': 'FCNantes'},
    'rcsaofficiel': {'tiktok': 'rcsaofficiel', 'twitter': 'RCSA'},
    'rclens': {'tiktok': 'rclens', 'twitter': 'RCLens'},
    'toulousefc': {'tiktok': 'toulousefc', 'twitter': 'ToulouseFC'},
    'staderennaisfc': {'tiktok': 'staderennaisfc', 'twitter': 'staderennais'},
    'sb29': {'tiktok': None, 'twitter': 'SB29'},
    'angerssco': {'tiktok': 'angerssco', 'twitter': 'AngersSCO'},
    'ajauxerre': {'tiktok': None, 'twitter': 'AJA'},
    'fclorient': {'tiktok': 'fclorient', 'twitter': 'FCLorient'},
    'parisfootballclub': {'tiktok': 'parisfootballclub', 'twitter': 'ParisFC'},
    'fcmetz': {'tiktok': 'fcmetz', 'twitter': 'FCMetz'},
}

print("Social media mapping created for", len(SOCIAL_MEDIA_MAP), "clubs")
print("\nSample mappings:")
for i, (ig, social) in enumerate(list(SOCIAL_MEDIA_MAP.items())[:5]):
    print(f"  {ig}: TikTok={social['tiktok']}, Twitter={social['twitter']}")

# Save for reference
with open('social-media-username-map.json', 'w') as f:
    json.dump(SOCIAL_MEDIA_MAP, f, indent=2)

print("\n✓ Mapping saved to social-media-username-map.json")
print("\nNext: Use this mapping to update club-data-real.ts")
