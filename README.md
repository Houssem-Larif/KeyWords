# KeyWords
a python package used to compute coupling between a given script and a set of transcripts

This Package takes as input the following:  
- an initial script
- a set of transcripts to be compared to the initial script
- a file containing stop words (insignificant words to be removed). This file must be named "stopWords.txt"

Istallation:
To install, just copy the "KeyWords" folder inside the "Lib" folder inside your python root.
Make sure the "KeyWords.py" file is well inside that folder, under "Lib"

Usage:
In order to use this, you need to have the needed files next to your test script.
The needed files are of course:
- the "stopWords.txt" file
- the script
- the transcripts
examples of those files exist inside the "KeyWords" folder, just copy them.

try this code in your test file:
```
from KeyWords import KeyWords
a = KeyWords.Kword("script.txt", "stopWords.txt")  
b = KeyWords.Kword("transcript_1.txt", "stopWords.txt")
print(a.computeKeyWords(100))  #this prints the top 100 keyWords from the file script.txt
print(b.computeKeyWords(100))  #this prints the top 100 keyWords from the file transcript_1.txt

#this compares top 100 key words from script.txt and key words from each one of the other files
comp = KeyWords.Comparer("script.txt", ["script.txt","transcript_1.txt","transcript_2.txt","transcript_3.txt"], 200)
```

the comparison function considers each file as a vector. it does the following:
- we consider the space formed from all the keywords coming either from the initial script or the transcript
- the occurance number of each key word in a given text is the projection of that vector on the space
- we compute the distance between two vectors as the euclidean distance.
- the resulting score that describes the difference between two files is actually that distance
