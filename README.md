# paatu-manager.exe

paatu-manager.exe is a Discord bot that seamlessly adds Spotify track links shared in the server to the designated Spotify accounts—administered by the server admin—or individual users' personal Spotify accounts, creating curated playlists in those accounts.

## Motivation

I developed this bot with the aim of enhancing music-sharing experiences within discord servers. Inspired by the numerous servers featuring dedicated channels for song sharing, I wanted to streamline the process of discovering new music. This solution eliminates the need to individually click and listen to songs, making music exploration more efficient and enjoyable for users.

## Features

| Features                        | v1  | v2  | v3  |
| ------------------------------- | --- | --- | --- |
| User-centric                    | ❌  | ✔   | ✔   |
| Server-centric                  | ❌  | ❌  | ✔   |
| Spotify                         | ✔   | ✔   | ✔   |
| YouTube                         | ❌  | ❌  | ❌  |
| Modularized, Clean Code         | ❌  | ❌  | ✔   |
| Do I have command over the bot? | ✔   | ✔   | ❌  |

- **Instant Addition to Playlists**: Spotify track links shared in the server are instantly added to playlists.
- **Multi-User Support**: Multiple users can log in, allowing songs to be added to their individual Spotify accounts too along with server's playlist.
- **In-Memory Data**: In-memory data ensures quick retrieval and safety, with no persistent data after bot restarts.
- **Data Privacy**: The specifics of stored data are obscured from visibility, enhancing user privacy.
- **Variable Deinitialization**: Variables are appropriately deinitialized during program execution and shutdown.
- **Encryption for Authentication Managers**: Spotify authentication managers are encrypted using Pickle for added security.
- **Temporary Feature Disablement**: The bot can be temporarily silenced, turning off the playlist addition feature.

### v1:

- Single-user login only, lacking server or user-centric features, focused solely on Spotify integration.
- Messy code from experimentation, facing deadends and learning through trial and error.
- Limited grasp on data handling, resulting in less-than-ideal code cleanliness.

### v2:

- Multi-user logins enabled, introducing class structures for better code organization.
- I have some control over the bot, with variable deinitialization and added encryption.
- Code is neater compared to v1, though still a work in progress.

### v3:

- Builds on v2 by becoming server-centric, supporting multiple servers and empowering server admins.
- Code modularized , used cogs, ensuring improved organization and encapsulation.
- Personal control sacrificed for enhanced modularity,security and specific server functionalities.

I attempted to add YouTube too, but the available Python wrappers and the Google Dev dashboard just didn't tickle my brain. So, for now, the YouTube feature is on the backburner. Stay tuned for the encore!

## Run Locally

If you are gonna fork or run this locally, you'll need to do create Spotify API keys, set up a Discord bot account, and make this .env file

```bash
SPOTIPY_CLIENT_ID =
SPOTIPY_CLIENT_SECRET =
SPOTIPY_REDIRECT_URI =

DISCORD_BOT_ID =

[KEY =]

[CREATOR_ID = ]
```

## Tech Stack

Python

## Credits
- [Hitesh](https://github.com/Hitesh1090) for inspiring me to create a Discord bot and assisting with its testing!

## Contact

I know, I didn't explain clearly how to use this bot exactly, so if you have doubts or just want to dive into the details, feel free to drop a line. Open an issue if you're feeling official, or hit me up on [Discord](https://discordapp.com/users/776722539211653151). Let's chat, troubleshoot, and make this bot dance to the right tunes together!
