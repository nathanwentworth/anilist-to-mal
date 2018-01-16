import requests
import pprint

query = '''
query ($username: String) {
  MediaListCollection(userName: $username, type: ANIME) {
    statusLists {
      progress
      score
      status
      notes
      repeat
      media {
        idMal
        episodes
        title { romaji }
      }
    }
  }
}
'''

# Define our query variables and values that will be used in the query request
variables = {
  'username': 'nathan'
}

url = 'https://graphql.anilist.co'

def main():
#   print('''
#                   ┏━━━━━━━━━━━━━━━━━━┓
#                   ┃  AniList to MAL  ┃
#                   ┗━━━━━━━━━━━━━━━━━━┛

# An export tool for Anilist to import to MyAnimeList.
# Enter your username, and this will generate a MyAnimeList
# compatible XML file to import at https://myanimelist.net/import.php

# Made by Nathan Wentworth (https://nathanwentworth.co)

# Report any problems to me on twitter! https://twitter.com/nathanwentworth
# ''')

  print('''
  ┏━━ AniList to MAL ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃ An export tool for Anilist to import to MyAnimeList.          ┃
  ┃ Enter your username, and this will generate an XML file       ┃
  ┃ to import here: https://myanimelist.net/import.php            ┃
  ┃ Made by Nathan Wentworth (https://nathanwentworth.co)         ┃
  ┃ Report any problems here: https://twitter.com/nathanwentworth ┃
  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
''')

  getUserData()

def getUserData():
  variables['username'] = input("→ Anilist username: ")

  if variables['username'] == '':
    print('Please enter a valid username!')
    getUserData()
  else:
    getAnilistData()

def getAnilistData():
  # Make the HTTP Api request
  response = requests.post(url, json={'query': query, 'variables': variables})
  jsonData = response.json()
  statusLists = jsonData['data']['MediaListCollection']['statusLists']
  printAniListData(statusLists)
  convertAnilistDataToXML(statusLists)

def printAniListData(data):
  print('↓ Exported List ↓')
  for listStatus in data:
    print('\n##### ' + listStatus.capitalize() + ' #####')
    for item in data[listStatus]:
      print(' - ' + str(item['media']['title']['romaji']))
  print('\n✔︎ Successfully exported!')
  print('\nGo to https://myanimelist.net/import.php and select "MyAnimeList Import" under import type.\n')

def convertAnilistDataToXML(data):
  output = '''<?xml version="1.0" encoding="UTF-8" ?>
    <!--
     Created by XML Export feature at MyAnimeList.net
     Programmed by Xinil
     Last updated 5/27/2008
    -->

    <myanimelist>

      <myinfo>
        <user_id>526891</user_id>
        <user_name>nathanwentworth</user_name>
        <user_export_type>1</user_export_type>
        <user_total_anime>357</user_total_anime>
        <user_total_watching>6</user_total_watching>
        <user_total_completed>150</user_total_completed>
        <user_total_onhold>14</user_total_onhold>
        <user_total_dropped>27</user_total_dropped>
        <user_total_plantowatch>160</user_total_plantowatch>
      </myinfo>

'''

  for listStatus in data:
    for item in data[listStatus]:
      s = str(item['status'])
      if s == "PLANNING":
        s = "Plan to Watch"
      elif s == "DROPPED":
        s = "Dropped"
      elif s == "CURRENT":
        s = "Watching"
      elif s == "PAUSED":
        s = "On-Hold"

      animeItem = ''
      animeItem += '        <anime>\n'
      animeItem += '          <series_animedb_id>' + str(item['media']['idMal']) + '</series_animedb_id>\n'
      animeItem += '          <series_episodes>' + str(item['media']['episodes']) + '</series_episodes>\n'
      animeItem += '          <my_watched_episodes>' + str(item['progress']) + '</my_watched_episodes>\n'
      animeItem += '          <my_score>' + str(item['score']) + '</my_score>\n'
      animeItem += '          <my_status>' + s + '</my_status>\n'
      animeItem += '          <my_times_watched>' + str(item['repeat']) + '</my_times_watched>\n'

      animeItem += '          <update_on_import>1</update_on_import>\n'
      animeItem += '        </anime>\n\n'

      output += animeItem

  output += '      </myanimelist>'

  writeToXMLFile(output)

def writeToXMLFile(output):
  f = open('anilist-export.xml', 'w')
  f.write(output)
  f.close()


main()
