import requests

class C2Profile:
    name = ''
    url = ''


    def __init__(self, name, url):
        self.name = name
        self.url = url


    def get_profile(self):
        r = requests.get(self.url)
        if r.status_code == 200:
            return r.content
        else:
            return


profiles = [
    C2Profile('virtuallythere', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/APT/apt1_virtuallythere.profile'),
    C2Profile('comfoo', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/APT/comfoo.profile'),
    C2Profile('etumbot', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/APT/etumbot.profile'),
    C2Profile('havex', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/APT/havex.profile'),
    C2Profile('meterpreter', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/APT/meterpreter.profile'),
    C2Profile('pittytiger', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/APT/pitty_tiger.profile'),
    C2Profile('putter', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/APT/putter.profile'),
    C2Profile('stringofpaerls', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/APT/string_of_paerls.profile'),
    C2Profile('taidoor', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/APT/taidoor.profile'),
    C2Profile('asprox', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/crimeware/asprox.profile'),
    C2Profile('backoff', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/crimeware/backoff.profile'),
    C2Profile('fiesta', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/crimeware/fiesta.profile'),
    C2Profile('fiesta2', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/crimeware/fiesta2.profile'),
    C2Profile('magnitude', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/crimeware/magnitude.profile'),
    C2Profile('zeus', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/crimeware/zeus.profile'),
    C2Profile('amazon', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/amazon.profile'),
    C2Profile('bingsearch', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/bingsearch_getonly.profile'),
    C2Profile('cnnvideo', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/cnnvideo_getonly.profile'),
    C2Profile('gmail', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/gmail.profile'),
    C2Profile('googledrive', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/googledrive_getonly.profile'),
    C2Profile('microsoftupdate', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/microsoftupdate_getonly.profile'),
    C2Profile('msnbcvideo', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/msnbcvideo_getonly.profile'),
    C2Profile('oscp', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/oscp.profile'),
    C2Profile('onedrive', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/onedrive_getonly.profile'),
    C2Profile('pandora', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/pandora.profile'),
    C2Profile('randomized', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/randomized.profile'),
    C2Profile('rtmp', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/rtmp.profile'),
    C2Profile('safebrowsing', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/safebrowsing.profile'),
    C2Profile('webbug', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/webbug.profile'),
    C2Profile('webbug_getonly', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/webbug_getonly.profile'),
    C2Profile('wikipedia', 'https://raw.githubusercontent.com/rsmudge/Malleable-C2-Profiles/master/normal/wikipedia_getonly.profile'),
]