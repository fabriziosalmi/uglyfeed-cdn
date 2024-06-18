import random
import wikipedia
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import logging
import argparse

# Step 1: Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Step 2: Parse Command-Line Arguments
parser = argparse.ArgumentParser(description='Generate RSS feeds for various astronomy topics from Wikipedia.')
parser.add_argument('--path', type=str, help='Output path for the RSS feeds directory.')
args = parser.parse_args()

# Step 3: Read Environment Variables
env_path = os.getenv('UNIVERSE_FEED_PATH')

# Determine the output path
output_path = args.path or env_path or './universe/'
logger.info(f'Output path for RSS feeds: {output_path}')

# Ensure the output directory exists
os.makedirs(output_path, exist_ok=True)

# Log the start of the script
logger.info("Script started")

# Define the main topics for each category
categories = {
    "astronomy_fact": ["Astronomy", "Cosmology", "Astrophysics"],
    "astronomical_event": ["Astronomical event", "Eclipse", "Meteor shower"],
    "planet": ["Planets of the Solar System", "Exoplanet"],
    "star": ["Star", "Binary star", "Supernova"],
    "galaxy": ["Galaxy", "Milky Way", "Andromeda Galaxy"],
    "constellation": ["Constellation", "Zodiac"],
    "asteroid_comet": ["Asteroid", "Comet"],
    "space_technology": ["Space technology", "Satellite", "Space probe"],
    "astronomer": ["Astronomer", "Astrophysicist"],
    "space_mission": ["Space mission", "Apollo program", "Mars rover"]
}

# Function to fetch related Wikipedia articles
def fetch_related_articles(main_topic):
    try:
        search_results = wikipedia.search(main_topic, results=20)
        return search_results
    except Exception as e:
        logger.error(f"Error fetching related articles for '{main_topic}': {e}")
        return []

# Function to fetch content from Wikipedia
def fetch_wikipedia_content(search_term):
    try:
        page = wikipedia.page(search_term)
        summary = page.summary
        url = page.url
        title = page.title
        return {"title": title, "summary": summary, "url": url}
    except wikipedia.exceptions.DisambiguationError as e:
        logger.warning(f"Disambiguation error for '{search_term}': {e}. Using first option '{e.options[0]}'")
        return fetch_wikipedia_content(e.options[0])
    except wikipedia.exceptions.PageError as e:
        logger.error(f"Page error for '{search_term}': {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error for '{search_term}': {e}")
        return None

# Step 4: Generate RSS feed item
def create_rss_item(content):
    logger.info(f"Creating RSS item for: {content['title']}")
    item = ET.Element('item')

    title_elem = ET.SubElement(item, 'title')
    title_elem.text = content['title']

    description_elem = ET.SubElement(item, 'description')
    description_elem.text = content['summary']

    link_elem = ET.SubElement(item, 'link')
    link_elem.text = content['url']

    pub_date_elem = ET.SubElement(item, 'pubDate')
    pub_date_elem.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    return item

# Step 5: Create RSS feed
def create_rss_feed(category, content):
    rss = ET.Element('rss')
    rss.set('version', '2.0')

    channel = ET.SubElement(rss, 'channel')

    title = ET.SubElement(channel, 'title')
    title.text = f'{category.replace("_", " ").capitalize()} of the Day'

    link = ET.SubElement(channel, 'link')
    link.text = f'http://example.com/{category}'  # Replace with a relevant link

    description = ET.SubElement(channel, 'description')
    description.text = f'RSS feed of the {category.replace("_", " ")} of the day.'

    rss_item = create_rss_item(content)
    channel.append(rss_item)

    return rss

# Step 6: Generate and save RSS feeds for each category
for category, main_topics in categories.items():
    logger.info(f"Generating RSS feed for {category}")
    # Fetch related articles for a randomly chosen main topic
    main_topic = random.choice(main_topics)
    related_articles = fetch_related_articles(main_topic)

    if related_articles:
        # Randomly select an article from the related articles
        search_term = random.choice(related_articles)
        content = fetch_wikipedia_content(search_term)

        if content:
            rss_feed = create_rss_feed(category, content)
            rss_feed_string = ET.tostring(rss_feed, encoding='unicode')

            category_output_path = os.path.join(output_path, f'{category}.xml')
            with open(category_output_path, 'w') as f:
                f.write(rss_feed_string)
            logger.info(f"RSS feed saved successfully to {category_output_path}")

# Log the end of the script
logger.info("Script ended")
