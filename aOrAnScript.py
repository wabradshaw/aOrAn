# This is a quick and dirty script that uses a corpus to decide whether or 
# not a pattern is most often used with 'a' or 'an'. The result is a file 
# containg the list of patterns that use 'an'. 
# 
# The script requires two source files, one containing 'an' data and one 
# containing 'a' data. Testing was done using the google ngrams data found at:
#
#   http://storage.googleapis.com/books/ngrams/books/datasetsv2.html
#
# Data for a/an can be extracted from there (a_ and an bigrams) using grep:
#
#   zgrep '^an .*' googlebooks-eng-all-2gram-20120701-an.gz > an.txt
#   zgrep '^a .*' googlebooks-eng-all-2gram-20120701-a_.gz > a.txt
# 
# Note that this regex doesn't include capitalised determiners, though not
# for any particular reason.
import re

an_file = 'an.txt'
a_file = 'a.txt'
output_file = 'anPatterns.json'
importance_threshold = 1000

print('Starting...')

an = dict()
with open(an_file, 'r') as file:
    for line in file:
        split = line.split('\t')
        word = split[0][3:]
        cleaned = re.sub('[^a-zA-Z]', '*', word)
        start = cleaned[:3]

        count = int(split[2])
        an[start] = an.get(start, 0) + count

with open(a_file, 'r') as file:
    for line in file:
        split = line.split('\t')
        word = split[0][2:]
        cleaned = re.sub('[^a-zA-Z]', '*', word)
        start = cleaned[:3]

        if start in an:
            count = int(split[2])
            an[start] = an.get(start, 0) -count

result = [key for key, count in an.items() if count > importance_threshold]

with open(output_file, 'w') as out:
    out.write("[")
    for pattern in sorted(result):
        out.write("\"" + pattern.strip() + "\",\n")
    out.write("\"\"]")

print(result)
print('Done')
