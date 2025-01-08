# total_query to OrderedDict
from collections import OrderedDict
from dataclasses import dataclass
from typing import List


total_query = {
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
        ],
        "remote_desktop": [
            '"Remote Desktop" connection interface',
            '"Remote Desktop" settings menu',
            '"Remote Desktop" file sharing interface',
            '"Remote Desktop" session toolbar',
            '"Remote Desktop" login screen'
        ],
        "deltaforce": [
            '"Deltaforce" antivirus dashboard',
            '"Deltaforce" real-time protection',
            '"Deltaforce" scan results screen',
            '"Deltaforce" quarantine view',
            '"Deltaforce" settings menu'
        ],
        "mcafee_ui_container": [
            '"McAfee" antivirus dashboard',
            '"McAfee" real-time protection screen',
            '"McAfee" scan results interface',
            '"McAfee" quarantine tools',
            '"McAfee" settings menu'
        ]
    }
}

@dataclass
class QueryInfo:
    cate: str
    cate_index: int
    app: str
    app_index: int
    query: str
    query_index: int

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}

    def __str__(self):
        output_str = f'{self.cate}-{self.app}-{self.query}'
        # remove \" and \'
        output_str = output_str.replace('\"', '')
        output_str = output_str.replace('\'', '')
        # replace ' ' with '_'
        output_str = output_str.replace(' ', '_')
        return output_str
    
    def path(self):
        output_str = f'{self.cate}/{self.app}/{self.query}'
        # remove \" and \'
        output_str = output_str.replace('\"', '')
        output_str = output_str.replace('\'', '')
        # replace ' ' with '_'
        output_str = output_str.replace(' ', '_')
        return output_str
    
    @property
    def index(self):
        return f'{self.cate_index:02d}_{self.app_index:02d}_{self.query_index:02d}'

CATE_LIST = []
APP_LIST= []
QUERY_LIST: List[QueryInfo] = []

def _build_list():
    global total_query
    org_dict = OrderedDict(total_query)
    
    for cate_index , (cate, apps) in enumerate(org_dict.items()):
        CATE_LIST.append({
            "cate" : cate,
            "cate_index": cate_index
        })
        for app_index ,(app, queries) in enumerate(apps.items()):
            APP_LIST.append({
                "cate" : cate,
                "cate_index": cate_index,
                "app" : app,
                "app_index": app_index
            })
            for query_index,query in enumerate(queries):
                QUERY_LIST.append(QueryInfo(**{
                    "cate" : cate,
                    "cate_index": cate_index,
                    "app" : app,
                    "app_index": app_index,
                    "query" : query,
                    'query_index': query_index
                }))

_build_list()

if __name__ ==  '__main__':
    print(f'category list with length: {len(CATE_LIST)}, {str(CATE_LIST[0])}')
    print(f'app list with length: {len(APP_LIST)}, {str(APP_LIST[0])}')
    print(f'query list with length: {len(QUERY_LIST)}, {str(QUERY_LIST[0])}')
    print(APP_LIST)