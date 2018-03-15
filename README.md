# PythonUtilities
Dumping repository for various utilities written in python. This repository currently contains:

  - [Download manager](https://github.com/guigzzz/PythonUtilities/blob/master/downloads.py)
  - [Progress Bar](https://github.com/guigzzz/PythonUtilities/blob/master/progress_bar.py)
  - [Set-Associative Cache](https://github.com/guigzzz/PythonUtilities/tree/master/Cache)
  
  
# Examples
 
## Download Manager

```
from downloads import Downloader
import sys

url = sys.argv[1]

d = Downloader(url)
d.download()
```

## Progress Bar

```
from progress_bar import ProgressBar
from time import sleep

# create progress bar object
pb = ProgressBar()

# progress bar wraps any iterator object
for i in pb(range(100)):
    sleep(0.03)
```

## Cache

```
from Cache import Cache
from Cache.replacement_algorithms import LRU

c = Cache(associativity = 4, number_sets = 1,
            key_type = int, value_type = int,
            replacement_policy = LRU)

def double(x):
    v = c[x]
    if v is None: # cache miss
        v = 2*x
        c[x] = v # write to cache

    return v

print([double(x) for x in range(10)])
print(c)    
```
This produces the following output:
```
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
Cache contents
   Set 0 - Contents: {6: 12, 7: 14, 8: 16, 9: 18}, current size: 4, max size: 4
```
