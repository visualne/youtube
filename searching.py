#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import ConfigParser

#ToDo
# Finish changeDate function


config = ConfigParser.ConfigParser()
config.read('credentials.txt')

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = config.get('configuration','api_key')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# Changes search results based on date published.
def changeDate(date=None):
  # Midnight EST on 8-4-2008
  # 2008-08-04T04:00:00.000
  # Midnight EST on 8-5-2008
  # 2008-08-04T04:00:00.000

  publishedAfter='2016-08-04T00:00:00Z'
  publishedBefore='2016-08-04T00:00:00Z'

  # Loop to create every hour in the day in GMT.
  for month in range(1,13):
    for day in range(32):
      for hour in range(24):
        # Loop to create every minute in the day in GMT.
        for minute in range(60):
          for second in range(60):
            # print '2016-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'T'+str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(second).zfill(2)

            publishedAfter = '2016-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'T'+str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(second).zfill(2)
            publishedBefore = '2016-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'T'+str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(second + 2).zfill(2)

            print 'Published Before: ' + publishedBefore + ' ' + 'Published After: ' + publishedAfter

  # Calling search with the above date
  # Need to search every hour every day for the whole day for a while year

  # Search every month 1-12
  # Search every hour 00:00 - 23:30
  # Search every minute 00 - 59



def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    type='video',
    part="id,snippet",
    publishedAfter='2012-08-04T00:00:00Z',
    publishedBefore='2012-08-05T00:00:00Z',
    maxResults=options.max_results
  ).execute()

  videos = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
      videos.append("%s (%s) (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"],
                                 search_result["snippet"]["channelId"]))


  print "Videos:\n", "\n".join(videos), "\n"


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=50)
  args = argparser.parse_args()

  try:
    changeDate()
    # youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
