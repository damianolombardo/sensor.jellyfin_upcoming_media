### Thank you to @gcorgnet for the original Emby media component. This is a direct fork for simple tweaks to enable Jellyfin, perhaps to be later merged into the Emby component for compatibility.

# Jellyfin Latest Media Component

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

Home Assistant component to feed [Upcoming Media Card](https://github.com/custom-cards/upcoming-media-card) with
the latest releases on an Jellyfin instance.</br>
This component does not require, nor conflict with, the default [Jellyfin](https://www.home-assistant.io/components/jellyfin/) component.</br></br>

### If you're having issues, check out the [troubleshooting guide](https://github.com/custom-cards/upcoming-media-card/blob/master/troubleshooting.md) before posting an issue or asking for help on the forums.

## Installation:

1. Install this component by copying [these files](https://github.com/jwillaz/sensor.jellyfin_upcoming_media/tree/master/custom_components/jellyfin_upcoming_media) to `/custom_components/jellyfin_upcoming_media/`.
2. Install the card: [Upcoming Media Card](https://github.com/custom-cards/upcoming-media-card)
3. Add the code to your `configuration.yaml` using the config options below.
4. Add the code for the card to your lovelace configuration.
5. **You will need to restart after installation for the component to start working.**

| key | default | required | description
| --- | --- | --- | ---
| api_key | | yes | Your Jellyfin API key
| user_id | | yes | The id of the user you want to impersonate. Note: this is an id, not a username. Spy on Jellyfin API calls to retrieve yours. </br>(The Libraries and Medias that get retrieved depend on what that user has access to)
| host | localhost | no | The host Jellyfin is running on.
| port | 8096 | no | The port Jellyfin is running on.
| ssl | false | no | Whether or not to use SSL for Jellyfin.
| max | 5 | no | Max number of items in sensor.
| use_backdrop | false | no | Defines whether to use the Backdrop Image, instead of the poster. (Great for using with the `fanart` display mode)
| include | | no | The names of the <strong>Jellyfin Libraries</strong> you want to include. If not specified, all libraries will be shown and this component will create one sensor per Library. This is language specific.
| group_libraries | false | no | This option generates only two sensors (jellyfin_latest_movies / jellyfin_latest_tv_shows), grouping all your movies and tv into seperate sensors despite library setup in Jellyfin. </br>This is useful for when Jellyfin has many libraries but you only want one sensor in Home Assistant.
| episodes | true | no | Setting this to false will change the items shown from Episodes to Seasons (for tv show libraries) and Songs to Albums (for music libraries).
</br>

**Do not just copy examples, please use config options above to build your own!**
### Sample for configuration.yaml:
> This will add items from the 'Movies', 'Kids Movies', 'TV Shows' and 'Music' Libraries in Jellyfin, as well as show seasons and albums for their respective libraries, creating a seperate sensor per library
```
sensor:
- platform: jellyfin_upcoming_media
  api_key: YOUR_JELLYFIN_API_KEY
  user_id: YOUR_JELLYFIN_USER_ID
  host: 192.168.1.4
  port: 8096
  ssl: True
  max: 5
  use_backdrop: true
  group_libraries: false
  episodes: false
  include:
    - Movies
    - Kids Movies
    - TV Shows
    - Music
```

> This will add all items Jellyfin and create one sensor for movies (jellyfin_latest_movies) and one for tv (jellyfin_latest_tv_shows)
```
sensor:
- platform: jellyfin_upcoming_media
  api_key: YOUR_JELLYFIN_API_KEY
  user_id: YOUR_JELLYFIN_USER_ID
  host: 192.168.1.4
  port: 8096
  ssl: True
  max: 5
  use_backdrop: true
  group_libraries: true
```
### Sample for ui-lovelace.yaml:

    - type: custom:upcoming-media-card
      entity: sensor.jellyfin_latest_movies
      title: Latest Movies


# Getting Information for the Plugin

## api_key
<ol>
  <li>Navigate to the Jellyfin Admin Dashboard (Cog in the top right)</li>
  <li>Select <strong>Api Keys</strong> from the side menu</li>
  <li>Select <strong>New Api Key</strong> from the top of the page</li>
</ol>

## user_id
### Via Web Interface
> This is just an example, make sure you get your own personal user_id
<ol>
  <li>Navigate to the Jellyfin Admin Dashboard (Cog in the top right)</li>
  <li>Select <strong>Users</strong> from the side menu</li>
  <li>Select the user you plan to use in HA from the list</li>
  <li>From the address bar you can get the user id </br>
  <i>http://jellyfin_host_ip:8096/jellyfin/web/#/dashboard/users/profile?userId=<strong>527563753xfd422288a32198522f821a</strong></i>
  </li>
</ol>

### Via API Interface
<ol>
  <li>Navigate to http://jellyfin_host_ip:8096/jellyfin/Users/Public</li>
  <li>You will be provided a JSON response containing all the users details</li>
  <li>Find the <strong>Name</strong> attribute for your user in the results</li>
  <li>Next to the Name you will see an attribute name <strong>ServerId</strong></li>
  <li>Next to the ServerId you will see <strong>Id</strong> - this is your user_id</li>
</ol>
