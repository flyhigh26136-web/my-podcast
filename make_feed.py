import os
import email.utils
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

BASE_URL = "https://flyhigh26136-web.github.io/my-podcast"
SHOW_TITLE = "Love and Loyalty"
AUTHOR = "flyhigh26136"
EMAIL = "flyhigh26136@gmail.com"
DESCRIPTION = "Video episodes hosted from Termux."
CATEGORY = "Society & Culture"

rss = ET.Element("rss", {
    "version": "2.0",
    "xmlns:itunes": "http://itunes.com",
    "xmlns:atom": "http://w3.org"
})

channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = SHOW_TITLE
ET.SubElement(channel, "link").text = BASE_URL
ET.SubElement(channel, "atom:link", {"href": f"{BASE_URL}/rss.xml", "rel": "self", "type": "application/rss+xml"})
ET.SubElement(channel, "language").text = "en-us"
ET.SubElement(channel, "description").text = DESCRIPTION

# Required Apple Podcasts tags
ET.SubElement(channel, "itunes:author").text = AUTHOR
ET.SubElement(channel, "itunes:summary").text = DESCRIPTION
ET.SubElement(channel, "itunes:explicit").text = "false"
ET.SubElement(channel, "itunes:category", {"text": CATEGORY})
ET.SubElement(channel, "itunes:image", {"href": f"{BASE_URL}/cover.jpg"})
owner = ET.SubElement(channel, "itunes:owner")
ET.SubElement(owner, "itunes:name").text = AUTHOR
ET.SubElement(owner, "itunes:email").text = EMAIL

for file in sorted(os.listdir(".")):
    if file.endswith((".mp3", ".mp4", ".m4a")):
        item = ET.SubElement(channel, "item")
        file_url = f"{BASE_URL}/{file}"
        ET.SubElement(item, "title").text = os.path.splitext(file)[0]
        ET.SubElement(item, "description").text = f"Episode: {file}"
        ET.SubElement(item, "link").text = file_url
        ET.SubElement(item, "guid", {"isPermaLink": "false"}).text = file_url
        ET.SubElement(item, "pubDate").text = email.utils.format_datetime(datetime.now(timezone.utc))
        mime_type = "video/mp4" if file.endswith(".mp4") else "audio/mpeg"
        ET.SubElement(item, "enclosure", {
            "url": file_url,
            "length": str(os.path.getsize(file)),
            "type": mime_type
        })
        ET.SubElement(item, "itunes:explicit").text = "false"

ET.indent(rss, space="  ")
tree = ET.ElementTree(rss)
tree.write("rss.xml", encoding="utf-8", xml_declaration=True)
print("rss.xml created successfully!")
