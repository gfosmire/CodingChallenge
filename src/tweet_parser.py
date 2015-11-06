#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a program that takes a text file of tweets in JSON
form, cleans up the text then writes the cleaned text with
the text's created_at timestamp to another text file. At the 
end of that file the number of non-ascii tweets is written.

Then the program creates a simple graph of the hashtags from
the tweets and calculates the average degree of each node
on a rolling one minute basis and writes the average degree
to another text file.

@author: George Fosmire
"""

import json 
import datetime

"""
Initialize the filepaths that will be used
"""
input_filename = './tweets_input/tweets.txt'
cleaned_tweets = './tweets_output/ft1.txt'
average_degree = './tweets_output/tf2.txt'

"""
Initialize the lists that will be used
"""
tweet_text = []
tweet_time = []
hashtags = []

"""
Initialize the graph as a dictionary
"""
graph = {}

"""
Initialize the variable that counts the number of unicode tweets
"""
unicode_tweets = 0

"""
Create datetime variable equal to one minute for the rolling
average calculation
"""
one_minute = datetime.timedelta(minutes=1)


"""
A simple function that determines if a string contains
any non-ascii characters by checking each chars dec value.
"""
def is_ascii(s):
    for c in s:
        if ord(c) > 127:                #check if char is outside ascii range
            return False
    return True

"""
A function that adds new nodes and/or edges to the graph,
first checking if they already exist. If they already
exist, the age of the node is updated in addtion to 
adding any new edges.
"""
def insert_node(tags,age):
    for tag in tags:                    #interate over all of the hashtags
        if tag in graph:                #check if the node already exists
            
            for i in range(len(tags)):         #if it does, add new edges
                if tag == tags[i]:      #a node can't be connected to itself
                    continue
                else:
                    for object in graph[tag]:
                        if object[0] == tag:
                            object[1] = age
                            break
                    graph[tag].add((tags[i],age))
                    
        
        else:                           #if the tag isn't already in the graph
            graph[tag] = set()          #initialize the key's value to a set

            for i in range(len(tags)):  #add edges, skipping self
                if tag == tags[i]:
                    continue
                else:
                    graph[tag].add((tags[i],age))


"""
A function that removes nodes and/or edges from the graph
by checking the age the edges. It does this by interating
over the entire graph, comparing the age of the edge to now,
and if it is older than one minute removing it. Then it checks
to see if the node is isolated, ie has no edges, and if it is
removes the node.
"""
def remove_node(now):
    old = now - one_minute              #the time to compare edges to
    old_nodes = []
    for node in graph:                  #interate over the graph
        old_edges = set()
        for object in graph[node]:      #check each edge
            if object[1] < old:
                old_edges.add(object)   #if edge is too old, add to list to be removed
        for object in old_edges:
            graph[node].discard(object) #remove old edges
        if len(graph[node]) == 0:       
             old_nodes.append(node)     #if node is isolated, add to list to be removed
    for object in old_nodes:
        del graph[object]               #remove isolated edges

"""
A funtion that calculates the average degree of a graph by
interating over the dictionary (graph) and adding up the
lengths of the values (edges) of each key (node) that isn't
a timestamp key.
"""
def avg_degree(gr):
    if len(gr) == 0:
        return 0.00
    edges = 0.
    for node in gr:                     #go over the whole graph
        edges += len(gr[node])          #add up all the edges
    avg_degree = edges / len(gr)        #divide by number of nodes
    return avg_degree

"""
The with statement below reads in the tweets.txt file,
grabbing the text, created_at, and hashtags, and saves
them each to their own list. The 'if limit' condition 
was needed to test my code with the provided tweets.txt,
but should not be needed for a file that contains only
JSON tweets. If the file this is tested on still contains
the artifacts from the API that fetched it, un comment
the lines.
"""
with open(input_filename, 'r') as infile:
    for line in infile:                 #go over the whole file
        raw_tweet = json.loads(line)    #decode the JSON
        if 'limit' in raw_tweet:
            continue
                                        #save the parts of the JSON we want
        tweet_text.append(raw_tweet['text'])
        tweet_time.append(raw_tweet['created_at'].encode('ascii','ignore'))
        hashtags.append(raw_tweet['entities']['hashtags'])
 
"""
The with statement below counts the number of non-ascii 
tweets, the writes the cleaned tweets and their created_at
timestamp to the ft1.txt output file. At the end of the 
file the number of non-ascii tweets is written.       
""" 
with open(cleaned_tweets, 'w') as outfile:
    for i in range(len(tweet_text)):    #go over every tweet
        if not is_ascii(tweet_text[i]): #increment if the tweet is non-ascii
            unicode_tweets += 1
                                        #clean the tweets up    
        outfile.write(tweet_text[i].encode('ascii','ignore').replace("\n"," ").replace("\t"," ") + ' (' + tweet_time[i] + ')\n')
    outfile.write('\n' + str(unicode_tweets) + ' tweets contained unicode.')
        

"""
The with statement below goes tweet by tweet adding tweets
that have more than one hashtag to the graph after cleaning
up the hashtag text. Regardless of if a tweet contained more
than one hashtag, every tweet's timestamp is fed to the
removal fuction to prune tweets older than one minute back
from 'now'. The the average degree of the graph is calculated,
and that is written to the output file. 
"""
with open(average_degree, 'w') as outfile:
    for i in range(len(hashtags)):      #go tweet by tweet
        avg_deg = 0.
        tags = []
                                        #make the timestamp a datetime object
        time = datetime.datetime.strptime(tweet_time[i], '%a %b %d %H:%M:%S +0000 %Y')
               
        for j in range(len(hashtags[i])):
            tags.append(hashtags[i][j]['text'].encode('ascii','ignore').strip().lower())
        
        tags = [x for x in tags if x != ''] #remove empty hashtags        
        
        if len(tags) > 1:               #only use tweets that contain more than one nonblank tag
            insert_node(tags, time)     #add nodes and edges with current time
        remove_node(time)               #give the removal function current time to delete old edges/nodes
        avg_deg = avg_degree(graph)
        outfile.write('{0:.2f}\n'.format(avg_deg))





