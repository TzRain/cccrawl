
import os
import re

def camel_to_snake(name):
    return re.sub(r'([A-Z])', r'_\1', name).lower()

def snake_to_camel(name):
    parts = name.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def name_to_path(name):
    name = name.replace('\"', '')
    name = name.replace('\'', '')
    return name.replace(' ', '_').lower()

"""
resolution = '1920x1080' # ...
language = 'en-us' # ...
theme = 'aero' # ...
app = 'excel' # ...

root_path = 'generativedatasets/generativedatasets/gold_en/collection=base/data/office/'

filename = f'{root_path}/resolution={resolution}/language={language}/theme={theme}/app={app}/'

"""

def generativedatasets_path_to_info(path):
    parts = path.split('/')
    resolution, language, theme, app = None, None, None, None
    for part in parts:
        if part.startswith('resolution='):
            resolution = part.split('=')[1]
        elif part.startswith('language='):
            language = part.split('=')[1]
        elif part.startswith('theme='):
            theme = part.split('=')[1]
        elif part.startswith('app='):
            app = part.split('=')[1]
    return {
        'resolution': resolution,
        'language': language,
        'theme': theme,
        'app': app
    }   

def generativedatasets_get_dir(root_path):
    resolutions = [d for d in os.listdir(root_path) if d.startswith('resolution=')]
    languages, themes, apps = set(), set(), set()
    dir_list = []
    for resolution in resolutions:
        resolution_path = os.path.join(root_path, resolution)
        for language in os.listdir(resolution_path):
            if language.startswith('language='):
                language_path = os.path.join(resolution_path, language)
                languages.add(language)
                for theme in os.listdir(language_path):
                    if theme.startswith('theme='):
                        theme_path = os.path.join(language_path, theme)
                        themes.add(theme)
                        for app in os.listdir(theme_path):
                            if app.startswith('app='):
                                dir_list.append(os.path.join(theme_path, app))
                                apps.add(app)

    resolutions = list(sorted(resolutions))
    languages = list(sorted(languages))
    themes = list(sorted(themes))
    apps = list(sorted(apps))

    meta = {
        'resolutions': resolutions,
        'languages': languages,
        'themes': themes,
        'apps': apps
    }
    return dir_list, meta