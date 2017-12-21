#!/usr/bin/env python2

import requests
import argparse
import pycurl
import os
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Downlad IMDB top 250 list')
parser.add_argument('-p', '--poster', help='Download posters of the movies too', action='store_true')
parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
parser.add_argument('-o', '--output', help='File to write the list')
args = parser.parse_args()

def dload(url, dest):
    fp = open(dest, 'wb')
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEDATA, fp)
    curl.perform()
    curl.close()
    fp.close()

def extract(rows):
    fp_list = open(args.output,'w')
    for mov in rows:
        name = mov.select('td.titleColumn')[0].get_text().replace('\n','').replace('      ','')
        rating = mov.select('td.imdbRating')[0].get_text().replace('\n','')
        rating = (' [' + rating.decode('utf8') +']').encode('utf8')
        filename = name + rating
        fp_list.write(filename.encode('utf8'))
        fp_list.write('\n')
        if args.verbose:
            print filename.encode('utf8')
        if args.poster:
            poster = mov.select('td a img')[0]['src']
            dload(poster, './posters/'+filename+'.jpg')
    fp_list.close()

def remove_posters():
    if not os.path.exists('./posters'):
        os.makedirs('./posters')
    else:
        for f in os.listdir('./posters/'):
            os.remove('./posters/'+f)

def retrieve():
    print '[INFO] Retreiving website'
    page = requests.get('http://www.imdb.com/chart/top')
    if int(page.status_code) == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        rows = soup.select('tbody.lister-list tr')
        print '[INFO] Successfully retrived' 
        print '[INFO] Cleaning previous list'
        if args.poster:
            remove_posters()
        print '[INFO] Successfully cleaned'

        print '[INFO] Downloading'
        extract(rows)
        print '[INFO] Successfully downloaded'

        print '[INFO] Finished. Exiting...'
if __name__ == '__main__':
    if args.output:
        if os.path.isfile(args.output):
            ans = raw_input('File exists.Overwrite? [y/n] : ')
            if ans == 'n':
                args.output = 'top-250.txt'
                print args.output
        elif os.path.exists(args.output):
            print 'Given filename points to a folder.Writing to \'top-250.txt\''
            args.output = 'top-250.txt'
    retrieve()
