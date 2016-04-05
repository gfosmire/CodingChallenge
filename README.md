# CodingChallenge
Insight Data Engineering Coding Challenge

This is a simple, single python 2.7 program approach to the coding challenge. Since this was a simple, one off project, I chose to hardcode the filepaths of the input and output, so the file structure was clearly described in the challenge. This means that run.sh only runs the python script, and doesn't pass it anything. I chose to solve this problem as it was presented, as opposed to how it might actually be impletmented in the real-world, with getting a data stream from an API. Because we were provided a text file with all of the tweets in it, it made more sense to do most of the preprocessing all at once, rather than go line by line. Most of the processing of the JSON tweets was fairly simple, as python has built in libraries to handle JSON and datetime stamps. Also, encoding the strings as ascii removed the majority of the escape characters. The only dependencies this program has are the libraries json and datetime, which to my knowledge come with every python distribution.

As for the graph of the hashtags, that was a little more challenging and fun. Instead of using or building a more standard graph class, I realized that there might be a simpler approach because the only desired information from the graph is its nodes average connectedness. I thought this would be a great job for a dictionary, with the keys as nodes and values as a set of edges. The rolling one minute average of degree proved to be the most challenging part. I solved this by making the values tuples, with one part being the hashtag (edge) and the other being the timestamp. If a new tweet came in with the same hashtag, the value was updated with the newer timestamp. Pruning edges that were too old, older than one minute, was fairly simple by spanning the graph in the form of iterating over the dictionary and comparing the timestamp. Edges that were more than a minute old were removed, and any node that contained no edges was also removed. Calculating the average degree of the graph was also fairly simple, just needing to interate over the dictionary and sum the length of the values (edges) then divide that by the length of the graph (number of nodes). Then it's a simple matter of doing this as each new tweet comes in and writing the average degree to the output file.

I believe that the data structure that I have created is rather elegant and easily scalable, but that it's implementation could be further refined. The insert_node() function works well and is quick. The remove_node() function is not as clean. I likely would have written it differently if I were working with a real data stream. In that case there would be easier ways to handle removing a node that are faster, and more scalable. I thought about trying to implement something closer to a real-world approach here, but the created_at timestamp of a tweet only has a one second resolution, so that means large numbers of tweets need to be removed at once. I thought about using the actual millisecond timestamp at the end of the JSON, but based on the wording of the challenge I thought a single average degree was wanted per text in at the one second level was wanted, so using the milliseconds would produce the wrong output for this.

Overall I really enjoyed this challenge, and had fun coming up with a pseudo graph made from a dictionary of strings, sets, and tuples.
