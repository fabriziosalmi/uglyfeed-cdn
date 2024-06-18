import wikipedia
from datetime import datetime
import xml.etree.ElementTree as ET
import logging
import argparse
import os
import yaml

# Step 1: Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Step 2: Parse Command-Line Arguments
parser = argparse.ArgumentParser(description='Generate RSS feed of WWII battles for today\'s date.')
parser.add_argument('--path', type=str, help='Output path for the RSS feed XML file.')
args = parser.parse_args()

# Step 3: Read Environment Variables
env_path = os.getenv('RSS_FEED_PATH')

# Step 4: Read from config.yaml
config_path = 'config.yaml'
config_yaml_path = None
if os.path.exists(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        config_yaml_path = config.get('feed_path')

# Determine the output path
output_path = args.path or env_path or config_yaml_path or './ww2_battles.xml'
logger.info(f'Output path for RSS feed: {output_path}')

# Log the start of the script
logger.info("Script started")

# Step 5: Get the current date and day of the month
today = datetime.now()
day_of_month = today.day
logger.info(f"Today's date: {today}, Day of month: {day_of_month}")

# Step 6: Search for battles
def search_battle(day_of_month):
    search_string = f"World War II battle {day_of_month}"
    logger.info(f"Searching for: {search_string}")
    try:
        search_results = wikipedia.search(search_string)
        logger.info(f"Search results: {search_results}")
        
        # Filter out non-battle entries, such as lists and general pages
        battle_results = [result for result in search_results if "battle" in result.lower() and "list" not in result.lower()]
        logger.info(f"Filtered battle results: {battle_results}")
        
        return battle_results
    except wikipedia.exceptions.DisambiguationError as e:
        logger.warning(f"Disambiguation error for search string '{search_string}': {e}")
        return e.options
    except wikipedia.exceptions.PageError:
        logger.error(f"No page found for search string '{search_string}'")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred during search: {e}")
        return []

# Step 7: Get the battle information
def get_battle_info(title):
    logger.info(f"Fetching information for battle title: {title}")
    try:
        page = wikipedia.page(title)
        logger.info(f"Fetched page: {page.url}")
        return page.summary, page.url
    except wikipedia.exceptions.DisambiguationError as e:
        logger.warning(f"Disambiguation error for title '{title}': {e}")
        # Try the first non-disambiguation option
        for option in e.options:
            try:
                page = wikipedia.page(option)
                logger.info(f"Resolved to page: {page.url}")
                return page.summary, page.url
            except Exception as inner_e:
                logger.warning(f"Error with option '{option}': {inner_e}")
                continue
        return None, None
    except wikipedia.exceptions.PageError:
        logger.error(f"No page found for title '{title}'")
        return None, None
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching page info: {e}")
        return None, None

# Step 8: Create an RSS item
def create_rss_item(title, description, link):
    logger.info(f"Creating RSS item for title: {title}")
    item = ET.Element('item')

    title_elem = ET.SubElement(item, 'title')
    title_elem.text = title

    description_elem = ET.SubElement(item, 'description')
    description_elem.text = description

    link_elem = ET.SubElement(item, 'link')
    link_elem.text = link

    return item

# Step 9: Create RSS feed
def create_rss_feed(items):
    rss = ET.Element('rss')
    rss.set('version', '2.0')
    
    channel = ET.SubElement(rss, 'channel')
    
    title = ET.SubElement(channel, 'title')
    title.text = 'World War II Battles on This Day'
    
    link = ET.SubElement(channel, 'link')
    link.text = 'http://example.com/ww2-battles'  # Replace with a relevant link
    
    description = ET.SubElement(channel, 'description')
    description.text = 'RSS feed of World War II battles that happened on this day of the month.'

    for item in items:
        channel.append(item)
    
    return rss

# Fetch battles and generate RSS items
battles = search_battle(day_of_month)

rss_items = []

if battles:
    # Prefer a title that starts with "Battle of" or similar specific battle name
    specific_battles = [title for title in battles if "Battle of" in title]
    if specific_battles:
        selected_battles = specific_battles
    else:
        selected_battles = battles  # Fall back to the filtered results if no specific battles found

    for battle_title in selected_battles:
        logger.info(f"Selected battle title: {battle_title}")
        battle_info, battle_url = get_battle_info(battle_title)
        
        if battle_info:
            rss_item = create_rss_item(battle_title, battle_info, battle_url)
            rss_items.append(rss_item)
            logger.info(f"RSS item created successfully for battle: {battle_title}")
        else:
            logger.error(f"No detailed information found for the battle: {battle_title}")
else:
    logger.error("No relevant battle found for today's date.")

if rss_items:
    rss_feed = create_rss_feed(rss_items)
    
    # Convert the RSS feed to a string
    rss_feed_string = ET.tostring(rss_feed, encoding='unicode')
    
    # Save the RSS feed to the specified output path
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(rss_feed_string)
    logger.info(f"RSS feed saved successfully to {output_path}")
else:
    logger.error("No RSS items to create a feed.")

# Log the end of the script
logger.info("Script ended")

