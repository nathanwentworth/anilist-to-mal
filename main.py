#!/usr/bin/env python3

import requests, pprint, sys, getopt

# Test query for https://anilist.co/graphiql
# {
#   MediaListCollection(userName: "nathan", type: ANIME) {
#     statusLists {
#       progress
#       score
#       status
#       notes
#       repeat
#       media {
#         idMal
#         episodes
#         title { romaji }
#       }
#     }
#   }
# }

# What kind of output do we want
outputFile = 'xml'
outputTxt = ''''''
silent = False
showProgress = False
name = 'anilist-export'

# Define our query variables and values that will be used in the query request
variables = {
  'username': '',
  'type': 'ANIME'
}

url = 'https://graphql.anilist.co'

def main(argv):
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

  global outputFile, silent, name, showProgress

  for index, arg in enumerate(argv):
    if arg == "-f" or arg == "--file":
      outputFile = argv[index + 1]
    elif arg == "-u":
      variables['username'] = argv[index + 1]
    elif arg == "-t":
      variables['type'] = argv[index + 1].upper()
    elif arg == "-s":
      silent = True
    elif arg == "-n":
      name = argv[index + 1]
    elif arg == "-p":
      showProgress = True

  if not silent:
    print('''
  ┏━━ AniList to MAL ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃ An export tool for Anilist to import to MyAnimeList.          ┃
  ┃ Enter your username, and this will generate an XML file       ┃
  ┃ to import here: https://myanimelist.net/import.php            ┃
  ┃ Made by Nathan Wentworth (https://nathanwentworth.co)         ┃
  ┃ Report any problems here: https://twitter.com/nathanwentworth ┃
  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
''')

  if variables['username'] == '':
    getUserData()
  elif variables['type'] == '':
    getListType()
  else:
    getAnilistData()

def getUserData():
  variables['username'] = input("→ Anilist username: ")

  if variables['username'] == '':
    print('Please enter a valid username!')
    getUserData()
  elif variables['type'] == '':
    getListType()
  else:
    getAnilistData()

def getListType():
  variables['type'] = input("→ List type (ANIME or MANGA): ").upper()

  if variables['type'] != 'ANIME' and variables['type'] != 'MANGA':
    print('Please enter either ANIME or MANGA')
    getListType()
  else:
    getAnilistData()

def getAnilistData():
  # Make the HTTP Api request
  query = '''
  query ($username: String, $type: MediaType) {
    MediaListCollection(userName: $username, type: $type) {
      statusLists {
        progress
        progressVolumes
        score(format: POINT_10)
        status
        notes
        repeat
        media {
          chapters
          volumes
          idMal
          episodes
          title { romaji }
        }
      }
    }
  }
  '''

  response = requests.post(url, json={'query': query, 'variables': variables})
  jsonData = response.json()

  if ('errors' in jsonData):
    for error in jsonData['errors']:
      print(error['message'])
    print('Your username may be incorrect, or Anilist might be down.')
    return

  statusLists = jsonData['data']['MediaListCollection']['statusLists']
  if len(statusLists) < 1:
    print('No items found in this list!\nDid you enter the wrong username?')
    return;
  if silent == False:
    convertAnilistDataToTxt(statusLists)
  if outputFile == 'xml':
    convertAnilistDataToXML(statusLists)
  elif outputFile == 'txt':
    if silent == True:
      convertAnilistDataToTxt(statusLists)
    writeToFile(outputTxt)

def convertAnilistDataToTxt(data):
  listOrder = ['current', 'completed', 'paused', 'planning', 'dropped']

  global outputTxt
  if variables['type'] == 'ANIME':
    outputTxt = "# Anime List\n"
  else:
    outputTxt = "# Manga List\n"

  for listStatus in listOrder:
    if listStatus in data:
      outputTxt += '\n## ' + listStatus.capitalize() + '\n'
      data[listStatus].sort(key=lambda show: show['score'], reverse=True)
      for item in data[listStatus]:
        outputTxt += '- '

        progress = '{0: >3}'.format(str(item['progress'])) + '/'
        progress += '{0: <3}'.format(str(item['media']['episodes']) if item['media']['episodes'] is not None else '??')
        if showProgress and listStatus == 'current' or listStatus == 'paused' or listStatus == 'dropped':
          outputTxt += progress + ' '
        else:
          outputTxt += '        ' # 8 characters, same as progress block

        title = str(item['media']['title']['romaji'])
        outputTxt += title

        if item['score'] > 0:
          outputTxt += '\tScore: ' + str(item['score']) + '/10'
        outputTxt += '\n'

  if not silent:
    print(outputTxt)

def convertAnilistDataToXML(data):
  output = ''''''
  user_total_anime = 0
  user_total_watching = 0
  user_total_completed = 0
  user_total_onhold = 0
  user_total_dropped = 0
  user_total_plantowatch = 0

  for listStatus in data:
    for item in data[listStatus]:
      s = str(item['status'])
      # print(s)
      if s == "PLANNING":
        if variables['type'] == 'ANIME':
          s = "Plan to Watch"
        else:
          s = "Plan to Read"
        user_total_plantowatch += 1
      elif s == "DROPPED":
        s = "Dropped"
        user_total_dropped += 1
      elif s == "CURRENT":
        if variables['type'] == 'ANIME':
          s = "Watching"
        else:
          s = "Reading"
        user_total_watching += 1
      elif s == "PAUSED":
        s = "On-Hold"
        user_total_onhold += 1
      elif "completed" in s.lower():
        s = "Completed"
        user_total_completed += 1

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
      user_total_anime += 1


  outputStart = '''<?xml version="1.0" encoding="UTF-8" ?>
    <!--
     Created by XML Export feature at MyAnimeList.net
     Programmed by Xinil
     Last updated 5/27/2008
    -->

    <myanimelist>

      <myinfo>
        <user_id>123456</user_id>
        <user_name>''' + variables['username'] + '''</user_name>
        <user_export_type>1</user_export_type>
        <user_total_anime>''' + str(user_total_anime) + '''</user_total_anime>
        <user_total_watching>''' + str(user_total_watching) + '''</user_total_watching>
        <user_total_completed>''' + str(user_total_completed) + '''</user_total_completed>
        <user_total_onhold>''' + str(user_total_onhold) + '''</user_total_onhold>
        <user_total_dropped>''' + str(user_total_dropped) + '''</user_total_dropped>
        <user_total_plantowatch>''' + str(user_total_plantowatch) + '''</user_total_plantowatch>
      </myinfo>

'''
  output = outputStart + output + '      </myanimelist>'

  writeToFile(output)

  if not silent:
    print('✔︎ Successfully exported!')
    print('\nGo to https://myanimelist.net/import.php and select "MyAnimeList Import" under import type.\n')


def writeToFile(output):
  f = open(name + variables['type'] + '.' + outputFile, 'w')
  f.write(output)
  f.close()

if __name__ == '__main__':
  main(sys.argv)
