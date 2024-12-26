import sys, os

if __name__ == "__main__":
    sys.path.append(os.getcwd())

import requests
from PIL import Image
from io import BytesIO
from dataclasses import dataclass
from collections import OrderedDict

from transformers import AutoModelForImageClassification,AutoImageProcessor
from PIL import Image
import requests
import torch

print(torch.cuda.is_available())
model = AutoModelForImageClassification.from_pretrained("al-css/Screenshots_detection_to_classification")
processor = AutoImageProcessor.from_pretrained("openai/clip-vit-base-patch32")

def check_is_screen(image):
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    probs = outputs[-1]
    return probs.softmax()[1]

# Define a dataclass to hold image information
@dataclass
class ImageData:
    identifier: str
    url: str

# Define the Bing Search API details
subscription_key = "b2df87ded3c7412e959be43508e0cd2b"
endpoint = "https://api.bing.microsoft.com/v7.0/images/search" # Replace with your endpoint, e.g., https://api.bing.microsoft.com/v7.0/images/search


QUERY_LIST = {
    "office_and_productivity": {
        "microsoft_word": [
            '"Microsoft Word" UI screenshot',
            '"Microsoft Word" ribbon menu interface',
            '"Microsoft Word" editing tools',
            'guide to "Microsoft Word" templates',
            '"Microsoft Word" document formatting'
        ],
        "microsoft_excel": [
            '"Microsoft Excel" spreadsheet interface',
            '"Microsoft Excel" pivot table tools',
            'data visualization in "Microsoft Excel"',
            '"Microsoft Excel" formulas editor',
            '"Microsoft Excel" chart creation UI'
        ],
        "microsoft_powerpoint": [
            '"Microsoft PowerPoint" slide editing',
            '"Microsoft PowerPoint" animation tools',
            'presenter mode in "Microsoft PowerPoint"',
            '"Microsoft PowerPoint" template gallery',
            'transitions in "Microsoft PowerPoint"'
        ],
        "microsoft_onedrive": [
            '"Microsoft OneDrive" cloud storage UI',
            '"Microsoft OneDrive" file sharing interface',
            '"Microsoft OneDrive" sync status',
            'access "Microsoft OneDrive" files',
            'shared folder in "Microsoft OneDrive"'
        ],
        "microsoft_teams": [
            '"Microsoft Teams" video conference UI',
            '"Microsoft Teams" chat interface',
            '"Microsoft Teams" channels overview',
            'calendar integration in "Microsoft Teams"',
            'file sharing via "Microsoft Teams"'
        ],
        "microsoft_outlook": [
            '"Microsoft Outlook" email interface',
            '"Microsoft Outlook" calendar view',
            '"Microsoft Outlook" contacts management',
            '"Microsoft Outlook" task list UI',
            '"Microsoft Outlook" folder organization'
        ],
        "adobe_acrobat": [
            '"Adobe Acrobat" PDF editor interface',
            '"Adobe Acrobat" tools pane',
            '"Adobe Acrobat" document view',
            '"Adobe Acrobat" annotation tools',
            '"Adobe Acrobat" form filling interface'
        ],
        "notion": [
            '"Notion" workspace interface',
            '"Notion" database view',
            '"Notion" project management dashboard',
            '"Notion" task list UI',
            '"Notion" collaborative editing'
        ],
        "trello": [
            '"Trello" board UI',
            '"Trello" task card view',
            '"Trello" workflow interface',
            '"Trello" calendar view',
            '"Trello" project management tools'
        ],
        "evernote": [
            '"Evernote" note editing interface',
            '"Evernote" notebook organization',
            '"Evernote" task management view',
            '"Evernote" tag management',
            '"Evernote" web clipper interface'
        ]
    },
    "media_playback_and_creation": {
        "vlc_media_player": [
            '"VLC Media Player" UI screenshot',
            '"VLC Media Player" playback controls',
            '"VLC Media Player" subtitle settings',
            'streaming via "VLC Media Player"',
            '"VLC Media Player" playlist view'
        ],
        "paint": [
            '"Microsoft Paint" UI screenshot',
            '"Microsoft Paint" toolbar layout',
            '"Microsoft Paint" drawing tools',
            '"Microsoft Paint" canvas workspace',
            '"Microsoft Paint" color palette'
        ],
        "adobe_photoshop": [
            '"Adobe Photoshop" editing workspace',
            '"Adobe Photoshop" layers panel',
            '"Adobe Photoshop" filters and effects',
            'color grading in "Adobe Photoshop"',
            '"Adobe Photoshop" tools interface'
        ],
        "adobe_premiere_pro": [
            '"Adobe Premiere Pro" timeline editing',
            '"Adobe Premiere Pro" workspace layout',
            '"Adobe Premiere Pro" color grading',
            '"Adobe Premiere Pro" audio tools',
            '"Adobe Premiere Pro" export settings'
        ],
        "spotify": [
            '"Spotify" music player UI',
            '"Spotify" playlist creation',
            '"Spotify" artist profile',
            '"Spotify" settings menu',
            '"Spotify" album library'
        ],
        "itunes": [
            '"iTunes" music library',
            '"iTunes" playlist management',
            '"iTunes" album cover view',
            '"iTunes" purchase history',
            '"iTunes" settings menu'
        ],
        "obs_studio": [
            '"OBS Studio" streaming setup',
            '"OBS Studio" recording settings',
            '"OBS Studio" audio mixer',
            '"OBS Studio" multi-scene editor',
            '"OBS Studio" interface overview'
        ],
        "davinci_resolve": [
            '"DaVinci Resolve" timeline tools',
            '"DaVinci Resolve" color grading workspace',
            '"DaVinci Resolve" fusion tab',
            '"DaVinci Resolve" audio editing tools',
            '"DaVinci Resolve" settings menu'
        ],
        "canva": [
            '"Canva" design tools',
            '"Canva" template library',
            '"Canva" collaboration features',
            '"Canva" text editing tools',
            '"Canva" element management'
        ],
        "final_cut_pro": [
            '"Final Cut Pro" timeline editing',
            '"Final Cut Pro" effects tools',
            '"Final Cut Pro" color correction',
            '"Final Cut Pro" audio settings',
            '"Final Cut Pro" export settings'
        ]
    },
    "gaming_and_game_platforms": {
        "steam": [
            '"Steam" library UI',
            '"Steam" store page layout',
            '"Steam" friends list',
            '"Steam" download management',
            '"Steam" settings menu'
        ],
        "epic_games_launcher": [
            '"Epic Games Launcher" library view',
            '"Epic Games Launcher" store interface',
            '"Epic Games Launcher" settings menu',
            '"Epic Games Launcher" downloads tab',
            '"Epic Games Launcher" promotions'
        ],
        "league_of_legends_client": [
            '"League of Legends" champion selection',
            '"League of Legends" match results',
            '"League of Legends" in-game HUD',
            '"League of Legends" profile page',
            '"League of Legends" settings'
        ],
        "roblox": [
            '"Roblox" game hub UI',
            '"Roblox" avatar customization',
            '"Roblox" developer tools',
            '"Roblox" in-game menu',
            '"Roblox" game creation'
        ],
        "valorant": [
            '"Valorant" agent selection',
            '"Valorant" game HUD',
            '"Valorant" scoreboard',
            '"Valorant" match history',
            '"Valorant" settings'
        ],
        "fortnite": [
            '"Fortnite" lobby UI',
            '"Fortnite" inventory management',
            '"Fortnite" game map overview',
            '"Fortnite" settings menu',
            '"Fortnite" in-game HUD'
        ],
        "dota_2": [
            '"Dota 2" hero selection',
            '"Dota 2" match stats',
            '"Dota 2" in-game HUD',
            '"Dota 2" item shop',
            '"Dota 2" settings menu'
        ],
        "minecraft": [
            '"Minecraft" crafting menu',
            '"Minecraft" survival HUD',
            '"Minecraft" world generation',
            '"Minecraft" inventory management',
            '"Minecraft" settings'
        ],
        "gog_galaxy": [
            '"GOG Galaxy" library UI',
            '"GOG Galaxy" store interface',
            '"GOG Galaxy" settings menu',
            '"GOG Galaxy" download manager',
            '"GOG Galaxy" friends list'
        ],
        "call_of_duty_warzone": [
            '"Call of Duty Warzone" lobby',
            '"Call of Duty Warzone" loadout menu',
            '"Call of Duty Warzone" HUD',
            '"Call of Duty Warzone" scoreboard',
            '"Call of Duty Warzone" settings'
        ]
    },
    "social_and_communication": {
        "discord": [
            '"Discord" server dashboard',
            '"Discord" text chat interface',
            '"Discord" voice channel',
            '"Discord" settings menu',
            '"Discord" activity feed'
        ],
        "zoom": [
            '"Zoom" video call interface',
            '"Zoom" participant view',
            '"Zoom" breakout room tools',
            '"Zoom" settings menu',
            '"Zoom" screen sharing'
        ],
        "whatsapp": [
            '"WhatsApp" chat interface',
            '"WhatsApp" group chats',
            '"WhatsApp" video calls',
            '"WhatsApp" settings menu',
            '"WhatsApp" media sharing'
        ],
        "telegram": [
            '"Telegram" chat UI',
            '"Telegram" bot commands',
            '"Telegram" group settings',
            '"Telegram" file sharing tools',
            '"Telegram" privacy settings'
        ],
        "wechat": [
            '"WeChat" messaging UI',
            '"WeChat" moments feed',
            '"WeChat" payment tools',
            '"WeChat" mini-programs',
            '"WeChat" settings menu'
        ],
        "slack": [
            '"Slack" workspace UI',
            '"Slack" threads interface',
            '"Slack" file sharing tools',
            '"Slack" integrations settings',
            '"Slack" notifications menu'
        ],
        "skype": [
            '"Skype" call interface',
            '"Skype" chat UI',
            '"Skype" group video calls',
            '"Skype" settings menu',
            '"Skype" contact management'
        ],
        "signal": [
            '"Signal" chat UI',
            '"Signal" disappearing messages',
            '"Signal" group chats',
            '"Signal" video calls',
            '"Signal" settings menu'
        ],
        "facebook_messenger": [
            '"Facebook Messenger" chat UI',
            '"Facebook Messenger" video calls',
            '"Facebook Messenger" group chats',
            '"Facebook Messenger" settings menu',
            '"Facebook Messenger" media sharing'
        ],
        "microsoft_teams": [
            '"Microsoft Teams" meetings',
            '"Microsoft Teams" chats',
            '"Microsoft Teams" channels',
            '"Microsoft Teams" file sharing',
            '"Microsoft Teams" settings'
        ]
    },
    "security_and_system_tools": {
        "windows_defender": [
            '"Windows Defender" dashboard',
            '"Windows Defender" scan results',
            '"Windows Defender" real-time protection',
            '"Windows Defender" quarantine',
            '"Windows Defender" settings menu'
        ],
        "ccleaner": [
            '"CCleaner" dashboard interface',
            '"CCleaner" junk file cleaner',
            '"CCleaner" registry cleaner',
            '"CCleaner" startup management',
            '"CCleaner" settings'
        ],
        "malwarebytes": [
            '"Malwarebytes" scan interface',
            '"Malwarebytes" threat detection',
            '"Malwarebytes" quarantine tools',
            '"Malwarebytes" real-time protection',
            '"Malwarebytes" settings menu'
        ],
        "windows_file_explorer": [
            '"Windows File Explorer" UI',
            '"Windows File Explorer" ribbon menu',
            '"Windows File Explorer" quick access',
            '"Windows File Explorer" properties window',
            '"Windows File Explorer" folder settings'
        ],
        "windows_control_panel": [
            '"Windows Control Panel" interface',
            '"Windows Control Panel" settings menu',
            '"Windows Control Panel" programs and features',
            '"Windows Control Panel" network settings',
            '"Windows Control Panel" user accounts'
        ],
        "windows_task_manager": [
            '"Windows Task Manager" processes tab',
            '"Windows Task Manager" performance tab',
            '"Windows Task Manager" startup programs',
            '"Windows Task Manager" details tab',
            '"Windows Task Manager" services tab'
        ],
        "windows_terminal": [
            '"Windows Terminal" main interface',
            '"Windows Terminal" PowerShell',
            '"Windows Terminal" command prompt',
            '"Windows Terminal" settings menu',
            '"Windows Terminal" themes'
        ],
        "revo_uninstaller": [
            '"Revo Uninstaller" dashboard',
            '"Revo Uninstaller" advanced scan',
            '"Revo Uninstaller" logs view',
            '"Revo Uninstaller" settings',
            '"Revo Uninstaller" software details'
        ],
        "vmware_workstation_player": [
            '"VMware Workstation Player" interface',
            '"VMware Workstation Player" virtual machine settings',
            '"VMware Workstation Player" snapshot tools',
            '"VMware Workstation Player" preferences menu',
            '"VMware Workstation Player" network settings'
        ],
        "powertoys": [
            '"PowerToys" main dashboard',
            '"PowerToys FancyZones" editor',
            '"PowerToys PowerRename" tool',
            '"PowerToys Color Picker"',
            '"PowerToys Keyboard Manager" settings'
        ]
    }
}



QUERY_LIST = OrderedDict(QUERY_LIST)

# Function to prepare search parameters dynamically
def prepare_search_params(query, min_width=None, max_width=None, min_height=None, max_height=None, **kwargs):
    params = {
        "q": query,
        "count": 16,  # Default number of results per request
        "offset": 0,
        # "license": "any",  # Example: public, share, sharecommercially, modify, modifycommercially
    }
    if min_width:
        params["minWidth"] = min_width
    if max_width:
        params["maxWidth"] = max_width
    if min_height:
        params["minHeight"] = min_height
    if max_height:
        params["maxHeight"] = max_height
    params.update(kwargs)  # Add additional dynamic parameters
    return params

# Function to search Bing for images with specific keywords and conditions
def bing_image_search(query, **search_params):
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = prepare_search_params(query, **search_params)

    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    search_results = response.json()

    print(search_results)

    # Extract image URLs, ensuring no duplicates
    web_pages_results = search_results['value']
    # filter out results without thumbnail URLs
    content_url = [res["contentUrl"] for res in web_pages_results if "contentUrl" in res]
    return content_url

# Function to handle multiple queries from a dictionary and generate indexed image URLs
def collect_image_urls(query_limit=5, **search_params):
    indexed_urls = []
    for app_index, (app_name, queries) in enumerate(QUERY_LIST.items()):
        for query_index, query in enumerate(queries[:query_limit]):
            print(f"Processing query: {query} for app: {app_name}")

            # Perform image search
            image_urls = bing_image_search(query, **search_params)

            # Assign index-based identifiers for app, query, and image
            for image_index, url in enumerate(image_urls):
                identifier = f"{app_index}_{query_index}_{image_index}"
                indexed_urls.append(ImageData(identifier, url))
    
    return indexed_urls

# Function to download images from indexed URLs
def download_images(indexed_urls, save_base_folder="bing_images"):
    os.makedirs(save_base_folder, exist_ok=True)

    for image_data in indexed_urls:
        try:
            response = requests.get(image_data.url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))

            flag = False

            if not check_is_screen(image):
                print(f"Skip: {image_data.url} is not a screen")
                flag = True

            sub_path = save_base_folder
            app_index, query_index, image_index = [ (int(x) if x.isdigit() else x) for x in image_data.identifier.split("_")]

            app = list(QUERY_LIST.keys())[app_index]
            query = QUERY_LIST[app][query_index]
            
            sub_path = os.path.join(sub_path, query.replace(" ","-"))
            os.makedirs(sub_path, exist_ok=True)

            
            if flag:
                save_path = os.path.join(sub_path, f"{image_data.identifier}_skip.jpeg")
            else:
                save_path = os.path.join(sub_path, f"{image_data.identifier}.jpeg")

            image.convert("RGB").save(save_path)

            print(f"Downloaded: {save_path}")
        except Exception as e:
            print(f"Failed to download {image_data.url}: {e}")

# Example usage
if __name__ == "__main__":

    sys.path.append(os.getcwd())

    search_params = {
        # "min_width": 300,  # Minimum width
        # "min_height": 300,  # Minimum height
        # "aspect": "wide",  # Example: wide images
        # "color": "colorOnly"  # Example: color-only images
    }
    # Limit each app to process up to 3 queries
    query_limit = 5

    print("Collecting all image URLs...")
    indexed_image_urls = collect_image_urls(query_limit=query_limit, **search_params)

    # for image_data in indexed_image_urls:
    #     print(f"{image_data.identifier}: {image_data.url}")

    print("Downloading images...")
    save_base_folder = './tmp/bing_images_any'
    os.makedirs(save_base_folder, exist_ok=True)
    download_images(indexed_image_urls,save_base_folder)

    print("All queries processed and images downloaded!")
