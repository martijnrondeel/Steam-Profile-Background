# Steam-Profile-Background
Get the background image from any public Steam profile page.

**Website:** https://martyn.pw/projects/steam-profile-background/  

--
**API Usage**  
Simply send a request to: https://martyn.pw/projects/steam-profile-background/api?url=profile_url_here

URL can be:
- ID URL (http://steamcommunity.com/id/Martyn96)
- Profiles URL (http://steamcommunity.com/profiles/76561198041914206)

**API Responses**  
- 200 Success, returns JSON with fields `imageURL` and `gameName`.
- 404 Not found, returns JSON with error and description for failed request. Possible errors are:
   - `INVALID_URL`, url was invalid
   - `NO_BACKGROUND`, profile had no background
   - `GAME_NOT_FOUND`, game that belongs to wallpaper doesn't exist (will still return image URL)
- 429 Too many requests, returns JSON with error and description for failed request. Possible errors are:
   - `RATELIMIT_EXCEEDED`, you sent more than 10 request in 1 minute

--

**Contributing**  
Please feel free to contribute! Most of this code was hacked together in one night, there's probably room for improvement :)
