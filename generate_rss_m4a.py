import os
import re
import datetime
import xml.etree.ElementTree as ET

# Configuration
BASE_URL = "https://amletdotco.github.io/918be8150a1bbeb28810b3135ce7ea7e42aa813c772d305ef9fefb7de0b29187/audio"  # Base URL for audio files
ARTWORK_URL = "https://amletdotco.github.io/918be8150a1bbeb28810b3135ce7ea7e42aa813c772d305ef9fefb7de0b29187/images/podcast_artwork.png"  # URL for podcast artwork
OUTPUT_FILE = "podcast_feed.xml"  # Output RSS file
PODCAST_TITLE = "John Flavel's The Fountain of Life"
PODCAST_DESCRIPTION = "A reading of John Flavel's The Fountain of Life"
PODCAST_LANGUAGE = "en-us"
PODCAST_LINK = "https://amletdotco.github.io/918be8150a1bbeb28810b3135ce7ea7e42aa813c772d305ef9fefb7de0b29187/"  # Podcast homepage


# Helper function to extract chapter number from file name
def extract_chapter_number(file_name):
    match = re.search(r"Chapter (\d+)", file_name)
    return (
        int(match.group(1)) if match else float("inf")
    )  # Default to infinity if no chapter number


# Generate the RSS feed
def generate_rss(audio_folder):
    # Create root RSS element
    rss = ET.Element(
        "rss",
        version="2.0",
        attrib={"xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"},
    )
    channel = ET.SubElement(rss, "channel")

    # Add podcast metadata
    ET.SubElement(channel, "title").text = PODCAST_TITLE
    ET.SubElement(channel, "link").text = PODCAST_LINK
    ET.SubElement(channel, "description").text = PODCAST_DESCRIPTION
    ET.SubElement(channel, "language").text = PODCAST_LANGUAGE
    ET.SubElement(channel, "itunes:image", href=ARTWORK_URL)  # Add podcast artwork

    # Get all audio files, sorted by chapter number
    audio_files = [
        file_name
        for file_name in os.listdir(audio_folder)
        if file_name.endswith(".m4a")
    ]
    audio_files.sort(key=extract_chapter_number)

    # Generate publish dates in ascending order
    base_date = datetime.datetime.now() - datetime.timedelta(
        days=len(audio_files) - 1
    )  # Subtract one less day so the latest episode is today
    for idx, file_name in enumerate(audio_files):
        file_path = os.path.join(audio_folder, file_name)
        file_url = f"{BASE_URL}/{file_name}"
        file_size = os.path.getsize(file_path)

        # Create an <item> element for each episode
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = os.path.splitext(file_name)[0]
        ET.SubElement(item, "description").text = f"Description for {file_name}"
        ET.SubElement(
            item,
            "enclosure",
            {"url": file_url, "length": str(file_size), "type": "audio/x-m4a"},
        )
        pub_date = (base_date + datetime.timedelta(days=idx)).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )
        ET.SubElement(item, "pubDate").text = pub_date

    # Write the RSS feed to the output file
    tree = ET.ElementTree(rss)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
    print(f"RSS feed generated: {OUTPUT_FILE}")


# Main script
if __name__ == "__main__":
    audio_folder = "audio"  # Path to your audio folder
    if not os.path.exists(audio_folder):
        print(f"Error: Folder '{audio_folder}' does not exist.")
    else:
        generate_rss(audio_folder)
