# Steam-Profile-Background
Get the background image from any public Steam profile page.

**Website:** https://martyn.me/projects/steam-profile-background/  

----
**API Usage**  
Simply send a request to: https://martyn.me/projects/steam-profile-background/api?url=profile_url_here

URL can be:
- ID URL (https://steamcommunity.com/id/lasermarty)
- Profiles URL (https://steamcommunity.com/profiles/76561198041914206)

**API Responses**  
- 200 Success, returns JSON with fields `imageURL` and `gameName`.
- 404 Not found, returns JSON with error and description for failed request. Possible errors are:
   - `INVALID_URL`, url was invalid
   - `NO_BACKGROUND`, profile had no background
   - `GAME_NOT_FOUND`, game that belongs to wallpaper doesn't exist (will still return image URL)
- 429 Too many requests, returns JSON with error and description for failed request. Possible errors are:
   - `RATELIMIT_EXCEEDED`, you sent more than 10 requests in 1 minute/200 requests in a day

----

**Contributing**  
Please feel free to contribute! Most of this code was hacked together in one night, there's probably room for improvement :)
