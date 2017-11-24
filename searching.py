#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import ConfigParser
import time
from datetime import datetime

#ToDo
# Change publishedAfter and publishedBefore timestamps so you are searching everyday
# for one year.
#Print the timestamps

# Finish changeDate function. Figure out how to create datetime object


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
def changeDate(options):
  # Midnight EST on 8-4-2008
  # 2008-08-04T04:00:00.000
  # Midnight EST on 8-5-2008
  # 2008-08-04T04:00:00.000

  # Loop to create every hour in the day in GMT.
  for month in range(2,13):
    # Loop to create every day in GMT.
    for day in range(1,31):
      # Loop to create ever hour in the day in GMT.
      for hour in range(23,24):


        # The below if statements need to be looked at. This is a weak attempt at dealing with months
        # with 29 and 30 days in them.
        if day + 1 == 30 and month == 2 and hour + 1 == 24:
          break
        # Dealing with 30 days in April
        elif day + 1 == 31 and month == 4 and hour + 1 == 24:
          break
        # Dealing with 30 days in June
        elif day + 1 == 31 and month == 6 and hours + 1 == 24:
          break
        # Dealing with 30 days in September
        elif day + 1 == 31 and month == 9 and hours + 1 == 24:
          break
        # Dealing with 30 days in November
        elif day + 1 == 31 and month == 11 and hours + 1 == 24:
          break
        else:
          publishedAfter = '2016-' + str(month).zfill(2) + '-' + str(day).zfill(2) + 'T' + str(hour).zfill(2) + ':' + '00' + ':' + '00' + 'Z'

          # Checking hour. If it is 23 we will break out of this for loop.
          if hour == 23:
            publishedBefore = '2016-' + str(month).zfill(2) + '-' + str(day + 1).zfill(2) + 'T' + '00' + ':' + '00' + ':' + '00' + 'Z'
          else:
            publishedBefore = '2016-' + str(month).zfill(2) + '-' + str(day).zfill(2) + 'T' + str(hour+1).zfill(2) + ':' + '00' + ':' + '00' + 'Z'


          # Call to youtube api here with the search parameters.
          youtube_search(options, publishedAfter, publishedBefore)


        # Loop to create every minute in the day in GMT.
        # for minute in range(60):
          # for second in range(59):
            # publishedAfter = '2016-' + str(month).zfill(2) + '-' + str(day).zfill(2) + 'T' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(second).zfill(2) + 'Z'
            # publishedBefore = '2016-' + str(month).zfill(2) + '-' + str(day).zfill(2) + 'T' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(second+1).zfill(2) + 'Z'

            # Call to youtube api here with the search parameters.
            # youtube_search(options,publishedAfter,publishedBefore)

            # Sleeping for one second
            # time.sleep(1)



        # Leaving for loop when minute == 22

def youtube_search(options,publishedAfterTimestamp=None,publishedBeforeTimestamp=None,nextPageToken=None):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Opening file handler
  f = open('Results.txt','w+')

  # 2016-01-01T00:00:02Z

  # Call the search.list method to retrieve results matching the specified query term.
  search_response = youtube.search().list(
    q=options.q,
    type='video',
    part="id,snippet",
    publishedAfter=publishedAfterTimestamp,
    publishedBefore=publishedBeforeTimestamp,
    maxResults=options.max_results
  ).execute()

  videos = []

  # Remove the below two lines
  total_results = search_response['pageInfo']['totalResults']
  next_page_token = search_response['nextPageToken']

  # print 'Published After: ' + publishedAfterTimestamp + ' ' + 'Published Before: ' + publishedBeforeTimestamp + ' Total Results: ' + str(total_results)


  # For loop to run through each new page worth of results
  for pageNum in range(total_results):
    if pageNum == 0:
      # Dealing with results on first page only
      for search_result in search_response.get("items", []):

        # Putting all the video search results into a list.
        videos.append("%s (%s) (%s) (%s) (%s)" % (search_result["snippet"]["title"],
                                        search_result["id"]["videoId"],
                                        search_result["snippet"]["channelId"],
                                        publishedAfterTimestamp,
                                        publishedBeforeTimestamp))

      # Checking size of videos list. If it is zero that means that ZERO results were found. This
      # is odd because the API is telling me that there are results......
      if len(videos) == 0:
        # breaking out of for loop
        break
      else:
        # print 'Published After: ' + publishedAfterTimestamp + ' ' + 'Published Before: ' + publishedBeforeTimestamp + ' Total Results: ' + str(total_results)
        # print "Videos:\n", "\n".join(videos), "\n"
        print "\n".join(videos), "\n"
        result = "Videos:\n", "\n".join(videos), "\n"
        # Writting videos found to output file.
        f.write("\n".join(videos).encode('utf-8'))

      # # Output string listed below.
      # outputString = "Videos:\n", "\n".join(videos), "\n"
      #
      # for result in videos:
      #   f.write(result.encode('utf-8') + '\n')


  # Closing output file.
  f.close()


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="nothing")
  argparser.add_argument("--max-results", help="Max results", default=50)
  args = argparser.parse_args()

  try:
    changeDate(args)
    # changeDate(args)
    # youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
