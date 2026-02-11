################################################################################
#                                                                              #
# With this code, you will be able to scrape the name, location, and date of   #
#                             each UFC event.                                  #
#                                                                              #
#                                                                              #
################################################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd

url_events = "http://ufcstats.com/statistics/events/completed?page=all"

# Fetch the page
response = requests.get(url_events)
page = BeautifulSoup(response.content, 'html.parser')

# Extract data
events_data = {
    'Event': [elem.text.strip() for elem in page.select(".b-link_style_black")],
    'Date': [elem.text.strip() for elem in page.select(".b-statistics__table-row .b-statistics__date")],
    'Place': [elem.text.strip() for elem in page.select(".b-statistics__table-row .b-statistics__table-col_style_big-top-padding")]
}

# Create DataFrame
events = pd.DataFrame(events_data)

################################################################################
#                                                                              #
# With this code, you will be able to scrape TOTALS AND  SIGNIFICANT STRIKES   # 
#                        tables form each fight.                               #
#                 This code could take a few minutes.                          #
#                                                                              #
#                                                                              #
################################################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "http://ufcstats.com/statistics/events/completed?page=all"
page = BeautifulSoup(requests.get(url).content, 'html.parser')

# Get event URLs
event = [link.get('href') for link in page.select(".b-link_style_black")]

# Initialize DataFrames
TOTALS = pd.DataFrame(columns=["Fighters", "Round", "KD", "Sig.Str.", "Sig.Str %", "Total Str", "TD", "TD %",
                                "Sub.Att", "Rev.", "Ctrl", "Method", "Until", "Until min", "Referee", "Format",
                                "Event Name", "Date", "Location"])

SIGNIFICANT_STRIKES = pd.DataFrame(columns=["Fighters", "SIG.STR", "Sig.Str%", "HEAD", "BODY", "LEG", "DISTANCE",
                                             "CLINCH", "GROUND", "Method", "Until", "Until min", "Referee", "Format",
                                             "Event Name", "Date", "Location"])

for i in range(len(event)):
    url_event = event[i]
    page_event = BeautifulSoup(requests.get(url_event).content, 'html.parser')
    
    # Get fight URLs from event page
    fight_rows = page_event.select('table tbody tr')
    fight_urls = [row.get('data-link') for row in fight_rows if row.get('data-link')]
    
    for j in range(len(fight_urls)):
        url_fight = fight_urls[j]
        
        # Fetch fight page
        page_fight = BeautifulSoup(requests.get(url_fight).content, 'html.parser')
        
        # Extract Round headers
        round_headers = [elem.text.strip() for elem in page_fight.select(".js-fight-section+ .js-fight-section .b-fight-details__table-row_type_head .b-fight-details__table-col")]
        lround = len(round_headers)
        
        # Duplicate rounds for both fighters
        Round_1_2 = round_headers * 2
        Round_1_2.sort(key=lambda x: round_headers.index(x))
        
        # Extract fight metadata
        method_elem = page_fight.select(".b-fight-details__label+ i")
        Method = [method_elem[0].text.strip() if method_elem else ""] * (lround * 2)
        
        until_elem = page_fight.select(".b-fight-details__text-item_first+ .b-fight-details__text-item")
        Until = [until_elem[0].text.strip() if until_elem else ""] * (lround * 2)
        
        until_min_elem = page_fight.select(".b-fight-details__text-item:nth-child(3)")
        Until_min = [until_min_elem[0].text.strip() if until_min_elem else ""] * (lround * 2)
        
        format_elem = page_fight.select(".b-fight-details__text-item:nth-child(4)")
        Format = [format_elem[0].text.strip() if format_elem else ""] * (lround * 2)
        
        referee_elem = page_fight.select("span")
        Referee = [referee_elem[0].text.strip() if referee_elem else ""] * (lround * 2)
        
        # Extract event information
        event_name_elem = page_event.select(".b-content__title-highlight")
        event_name = [event_name_elem[0].text.strip() if event_name_elem else ""] * (lround * 2)
        
        event_date_elem = page_event.select(".b-list__box-list-item:nth-child(1)")
        event_date = [event_date_elem[0].text.strip() if event_date_elem else ""] * (lround * 2)
        
        event_location_elem = page_event.select(".b-list__box-list-item+ .b-list__box-list-item")
        event_location = [event_location_elem[0].text.strip() if event_location_elem else ""] * (lround * 2)
        
        # Extract TOTALS table data
        fighters = [elem.text.strip() for elem in page_fight.select(".js-fight-section+ .js-fight-section .js-fight-table .l-page_align_left .b-fight-details__table-text")]
        kd = [elem.text.strip() for elem in page_fight.select(".js-fight-section+ .js-fight-section .js-fight-table .l-page_align_left+ .b-fight-details__table-col .b-fight-details__table-text")]
        sig_str = [elem.text.strip() for elem in page_fight.select(".js-fight-section+ .js-fight-section .js-fight-table .b-fight-details__table-col:nth-child(3) .b-fight-details__table-text")]
        sig_str_pct = [elem.text.strip() for elem in page_fight.select(".js-fight-section+ .js-fight-section .js-fight-table .b-fight-details__table-col:nth-child(4) .b-fight-details__table-text")]
        total_str = [elem.text.strip() for elem in page_fight.select(".js-fight-section+ .js-fight-section .js-fight-table .b-fight-details__table-col:nth-child(5) .b-fight-details__table-text")]
        td = [elem.text.strip() for elem in page_fight.select(".js-fight-section+ .js-fight-section .js-fight-table .b-fight-details__table-col:nth-child(6) .b-fight-details__table-text")]
        td_pct = [elem.text.strip() for elem in page_fight.select(".js-fight-section+ .js-fight-section .js-fight-table .b-fight-details__table-col:nth-child(7) .b-fight-details__table-text")]
        sub_att = [elem.text.strip() for elem in page_fight.select(".js-fight-section+ .js-fight-section .js-fight-table .b-fight-details__table-col:nth-child(8) .b-fight-details__table-text")]
        rev = [elem.text.strip() for elem in page_fight.select(".js-fight-section+ .js-fight-section .js-fight-table .b-fight-details__table-col:nth-child(9) .b-fight-details__table-text")]
        ctrl = [elem.text.strip() for elem in page_fight.select(".js-fight-table .b-fight-details__table-col:nth-child(10) .b-fight-details__table-text")]
        
        table1_fights = pd.DataFrame({
            "Fighters": fighters,
            "Round": Round_1_2,
            "KD": kd,
            "Sig.Str.": sig_str,
            "Sig.Str %": sig_str_pct,
            "Total Str": total_str,
            "TD": td,
            "TD %": td_pct,
            "Sub.Att": sub_att,
            "Rev.": rev,
            "Ctrl": ctrl,
            "Method": Method,
            "Until": Until,
            "Until min": Until_min,
            "Referee": Referee,
            "Format": Format,
            "Event Name": event_name,
            "Date": event_date,
            "Location": event_location
        })
        
        # Extract SIGNIFICANT STRIKES table data
        fighters2 = [elem.text.strip() for elem in page_fight.select("table+ .js-fight-section .b-link_style_black")]
        sig_str2 = [elem.text.strip() for elem in page_fight.select("table+ .js-fight-section .l-page_align_left+ .b-fight-details__table-col .b-fight-details__table-text")]
        sig_str_pct2 = [elem.text.strip() for elem in page_fight.select("table+ .js-fight-section .b-fight-details__table-col:nth-child(3) .b-fight-details__table-text")]
        head = [elem.text.strip() for elem in page_fight.select("table+ .js-fight-section .b-fight-details__table-col:nth-child(4) .b-fight-details__table-text")]
        body = [elem.text.strip() for elem in page_fight.select("table+ .js-fight-section .b-fight-details__table-col:nth-child(5) .b-fight-details__table-text")]
        leg = [elem.text.strip() for elem in page_fight.select("table+ .js-fight-section .b-fight-details__table-col:nth-child(6) .b-fight-details__table-text")]
        distance = [elem.text.strip() for elem in page_fight.select("table+ .js-fight-section .b-fight-details__table-col:nth-child(7) .b-fight-details__table-text")]
        clinch = [elem.text.strip() for elem in page_fight.select("table+ .js-fight-section .b-fight-details__table-col:nth-child(8) .b-fight-details__table-text")]
        ground = [elem.text.strip() for elem in page_fight.select("table+ .js-fight-section .b-fight-details__table-col:nth-child(9) .b-fight-details__table-text")]
        
        table2_fights = pd.DataFrame({
            "Fighters": fighters2,
            "SIG.STR": sig_str2,
            "Sig.Str%": sig_str_pct2,
            "HEAD": head,
            "BODY": body,
            "LEG": leg,
            "DISTANCE": distance,
            "CLINCH": clinch,
            "GROUND": ground,
            "Method": Method,
            "Until": Until,
            "Until min": Until_min,
            "Referee": Referee,
            "Format": Format,
            "Event Name": event_name,
            "Date": event_date,
            "Location": event_location
        })
        
        # Append to main DataFrames
        TOTALS = pd.concat([TOTALS, table1_fights], ignore_index=True)
        SIGNIFICANT_STRIKES = pd.concat([SIGNIFICANT_STRIKES, table2_fights], ignore_index=True)
        
        # Optional: Add small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    # Progress indicator
    print(f"Processed event {i+1}/{len(event)}")

# Display results
print("\nTOTALS:")

print(f"\nTotal rows: {len(TOTALS)}")

print("\nSIGNIFICANT STRIKES:")
print(f"\nTotal rows: {len(SIGNIFICANT_STRIKES)}")



################################################################################
#                                                                              #
#     With this code, you will be able to scrape information about each        #
#                fight card and each fight on the card.                        #
#                                                                              #
################################################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

url_events = "http://ufcstats.com/statistics/events/completed?page=all"
page_events = BeautifulSoup(requests.get(url_events).content, 'html.parser')

# Get event URLs
event = [link.get('href') for link in page_events.select(".b-link_style_black")]
le = len(event)

def function_Main_Card(events):
    """
    Scrape main card information for all UFC events
    """
    all_main_cards = pd.DataFrame(columns=["Event", "Date", "Place", "Fighter", "KD", "STR", "TD", "SUB", 
                                            "WEIGHT.CLASS", "METHOD", "ROUND", "TIME", "RESULT"])
    
    for i in range(le):
        url_func = events[i]
        page = BeautifulSoup(requests.get(url_func).content, 'html.parser')
        
        # Extract WEIGHT CLASS
        WEIGHT_CLASS1 = [elem.text.strip() for elem in page.select(".l-page_align_left:nth-child(7) .b-fight-details__table-text")]
        lv = len(WEIGHT_CLASS1)
        
        # Duplicate for both fighters and interleave
        WEIGHT_CLASS1 = [val for val in WEIGHT_CLASS1 for _ in range(2)]
        
        # Extract METHOD
        METHOD1 = [elem.text.strip() for elem in page.select(".js-fight-details-click .l-page_align_left+ .l-page_align_left")]
        METHOD1 = [val for val in METHOD1 for _ in range(2)]
        
        # Extract ROUND
        ROUND1 = [elem.text.strip() for elem in page.select(".b-fight-details__table-col:nth-child(9) .b-fight-details__table-text")]
        ROUND1 = [val for val in ROUND1 for _ in range(2)]
        
        # Extract TIME
        TIME1 = [elem.text.strip() for elem in page.select(".b-fight-details__table-col:nth-child(10) .b-fight-details__table-text")]
        TIME1 = [val for val in TIME1 for _ in range(2)]
        
        # Extract event information
        event_name_elem = page.select(".b-content__title-highlight")
        event_name = event_name_elem[0].text.strip() if event_name_elem else ""
        
        event_date_elem = page.select(".b-list__box-list-item:nth-child(1)")
        event_date = event_date_elem[0].text.strip() if event_date_elem else ""
        
        event_place_elem = page.select(".b-list__box-list-item+ .b-list__box-list-item")
        event_place = event_place_elem[0].text.strip() if event_place_elem else ""
        
        # Extract results (win/lose flags)
        res = [elem.text.strip() for elem in page.select(".b-fight-details__table-text:nth-child(1) .b-flag__text")]
        lr = len(res)
        
        # Duplicate results
        result = res + res
        
        # Sort to interleave
        result_df = pd.DataFrame({
            'Result': result,
            'index': list(range(lr)) * 2
        })
        result_df = result_df.sort_values('index').reset_index(drop=True)
        
        RESULT = result_df['Result'].tolist()
        
        # Assign lose to opponent when fighter wins
        ld = len(RESULT)
        for j in range(0, ld, 2):
            if RESULT[j] == "win":
                RESULT[j + 1] = "lose"
        
        # Extract fighter stats
        fighters = [elem.text.strip() for elem in page.select(".b-link_style_black")]
        KD = [elem.text.strip() for elem in page.select(".b-fight-details__table-col:nth-child(3) .b-fight-details__table-text")]
        STR = [elem.text.strip() for elem in page.select(".b-fight-details__table-col:nth-child(4) .b-fight-details__table-text")]
        TD = [elem.text.strip() for elem in page.select(".b-fight-details__table-col:nth-child(5) .b-fight-details__table-text")]
        SUB = [elem.text.strip() for elem in page.select(".b-fight-details__table-col:nth-child(6) .b-fight-details__table-text")]
        
        # Create DataFrame for this event
        main_event = pd.DataFrame({
            "Event": [event_name] * len(fighters),
            "Date": [event_date] * len(fighters),
            "Place": [event_place] * len(fighters),
            "Fighter": fighters,
            "KD": KD,
            "STR": STR,
            "TD": TD,
            "SUB": SUB,
            "WEIGHT.CLASS": WEIGHT_CLASS1,
            "METHOD": METHOD1,
            "ROUND": ROUND1,
            "TIME": TIME1,
            "RESULT": RESULT
        })
        
        # Append to main DataFrame
        all_main_cards = pd.concat([all_main_cards, main_event], ignore_index=True)
        
        # Progress indicator
        print(f"Processed event {i+1}/{le}")
        
        # Optional: Add delay to avoid overwhelming the server
        time.sleep(0.5)
    
    return all_main_cards

# Execute the function
main_card_table = function_Main_Card(event)

# Display results
print("\nMain Card Table:")
print(f"\nTotal rows: {len(main_card_table)}")

################################################################################
#                                                                              #
#     With this code, you will be able to scrape information about each        #
#                             fighter (NO LXML REQUIRED)                       #
#                                                                              #
################################################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
import re
import time

def scrape_fighters():
    """Scrape all UFC fighters from A-Z"""
    base_url = "http://ufcstats.com/statistics/fighters?char={}&page=all"
    all_fighters = []
    
    for char in string.ascii_lowercase:
        print(f"Scraping fighters: {char.upper()}...", end=' ')
        
        try:
            response = requests.get(base_url.format(char))
            page = BeautifulSoup(response.content, 'html.parser')
            
            # Find the table
            table = page.select_one("table.b-statistics__table tbody")
            if not table:
                print("✗ No table found")
                continue
            
            # Extract data manually from table rows
            rows = table.find_all('tr')
            fighters_data = []
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 10:  # Make sure we have enough columns
                    fighter_data = {
                        'First': cols[0].text.strip(),
                        'Last': cols[1].text.strip(),
                        'Nickname': cols[2].text.strip(),
                        'Ht.': cols[3].text.strip(),
                        'Wt.': cols[4].text.strip(),
                        'Reach': cols[5].text.strip(),
                        'Stance': cols[6].text.strip(),
                        'W': cols[7].text.strip(),
                        'L': cols[8].text.strip(),
                        'D': cols[9].text.strip()
                    }
                    fighters_data.append(fighter_data)
            
            if fighters_data:
                df = pd.DataFrame(fighters_data)
                all_fighters.append(df)
                print(f"✓ ({len(fighters_data)} fighters)")
            else:
                print("✗ No data extracted")
            
            time.sleep(0.3)  # Be respectful to server
            
        except Exception as e:
            print(f"✗ Error: {e}")
            continue
    
    # Combine all DataFrames
    if all_fighters:
        fighters = pd.concat(all_fighters, ignore_index=True)
        return fighters
    else:
        return pd.DataFrame()

def process_height(height_str):
    """Extract feet and inches from height string like 5' 11\""""
    if height_str == "--" or pd.isna(height_str) or height_str == "":
        return None, None
    
    try:
        # Extract feet (first digit before ')
        feet_match = re.search(r"(\d+)'", height_str)
        # Extract inches (digits before ")
        inches_match = re.search(r"\s(\d+)\"", height_str)
        
        feet = int(feet_match.group(1)) if feet_match else None
        inches = int(inches_match.group(1)) if inches_match else None
        
        return feet, inches
    except:
        return None, None

def clean_fighters_data(df):
    """Clean and process fighter data"""
    if df.empty:
        return df
    
    # Process height
    df[['Foot', 'Inches']] = df['Ht.'].apply(
        lambda x: pd.Series(process_height(x))
    )
    
    # Calculate height in cm
    df['Height_cm'] = ((df['Foot'] * 12) + df['Inches']) * 2.54
    
    # Extract weight in pounds
    df['Weight.Lbs'] = df['Wt.'].str.extract(r'(\d+)')[0]
    df['Weight.Lbs'] = pd.to_numeric(df['Weight.Lbs'], errors='coerce')
    
    # Convert to kg
    df['Weight.Kg'] = df['Weight.Lbs'] * 0.453592
    
    # Convert W, L, D to numeric
    df['W'] = pd.to_numeric(df['W'], errors='coerce')
    df['L'] = pd.to_numeric(df['L'], errors='coerce')
    df['D'] = pd.to_numeric(df['D'], errors='coerce')
    
    return df

# Main execution
print("Starting UFC fighters scrape...\n")
fighters_raw = scrape_fighters()

if fighters_raw.empty:
    print("\n✗ No data was scraped. Please check your internet connection.")
else:
    print(f"\n✓ Total fighters scraped: {len(fighters_raw)}\n")
    
    print("Processing fighter data...")
    data_fighters_final = clean_fighters_data(fighters_raw)
    
    # Display results
    print("\n" + "="*80)
    print("FIGHTER DATA SUMMARY")
    print("="*80)
    print(f"Total fighters: {len(data_fighters_final)}")
    print(f"\nColumns: {', '.join(data_fighters_final.columns)}")
    print("\nSample data:")
    print(data_fighters_final[['First', 'Last', 'Ht.', 'Height_cm', 'Wt.', 'Weight.Kg', 'W', 'L', 'D']].head(10))
    
    # Display statistics
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Average Height: {data_fighters_final['Height_cm'].mean():.2f} cm")
    print(f"Average Weight: {data_fighters_final['Weight.Kg'].mean():.2f} kg")
    print(f"Total Wins: {data_fighters_final['W'].sum():.0f}")
    print(f"Total Losses: {data_fighters_final['L'].sum():.0f}")
    print(f"Total Draws: {data_fighters_final['D'].sum():.0f}")