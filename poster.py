#!/usr/bin/env python

from urllib2 import urlopen
import re
from time import sleep

import praw
from praw import errors


USERNAME = ''
PASSWORD = ''

def get_feed():
    url = 'http://www.huffingtonpost.com/feeds/verticals/technology/news.xml'
    content = urlopen(url).read()
            
    title_finder = re.compile('<title>(.*)</title>')
    link_finder = re.compile('<link rel="alternate" type="text/html" href="(.*)\?utm_.*/>')
    
    titles = re.findall(title_finder, content)[1:] # skip page title
    links = re.findall(link_finder, content)
    
    return titles, links

if __name__ == '__main__':
    
    print 'Scraping HuffPo feed...'
    # scrape HuffPo to get latest tech articles
    titles, links = get_feed()
    print 'Found %d articles...' % len(titles)

    # post to reddit
    r = praw.Reddit(user_agent='Tech news submitter by /u/Tech_Poster')
    try:
        print 'Logging in to reddit...'
        r.login(USERNAME, PASSWORD)
        print '\tLogin successful...'
    except errors.InvalidUserPass:
        print 'Wrong login details for reddit.'
    else:
        # post the latest articles on reddit
        for i in range(min(len(titles), len(links))):
            try:
                print 'Submitting %s' % links[i]
                r.submit('technology', titles[i], url=links[i])
                print '\tSubmission successful. Sleeping for 10 minutes'
                sleep(600) # wait for 10 minutes before submitting again
            except errors.ExceptionList as e_list:
                for e in e_list:
                    print e + ': ' + e.message
                pass
            except errors.AlreadySubmitted as e:
                print e
                pass
            except errors.RateLimitExceeded as e:
                print e
                print 'Sleeping for 10 minutes'
                sleep(600) # wait for 11 minutes before submitting again
                pass