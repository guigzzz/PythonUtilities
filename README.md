# PythonUtilities
Dumping repository for various utilities written in python. This repository currently contains:

  - [Download manager](https://github.com/guigzzz/PythonUtilities/blob/master/downloads.py)
  - [Progress Bar](https://github.com/guigzzz/PythonUtilities/blob/master/progress_bar.py)
  - [Set-Associative Cache](https://github.com/guigzzz/PythonUtilities/tree/master/Cache)
  - [Pip package upgrade utility](https://github.com/guigzzz/PythonUtilities/blob/master/pipupdater.py)
  
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

## Pipupdater

Example:
Assuming the following is the output of `python pipupdater.py --show`
```
0 - decorator: 4.1.2 -> 4.2.1 [wheel]
1 - ipykernel: 4.6.1 -> 4.8.2 [wheel]
2 - ipywidgets: 7.0.4 -> 7.1.2 [wheel]
3 - jedi: 0.11.0 -> 0.11.1 [wheel]
4 - jupyter-client: 5.1.0 -> 5.2.3 [wheel]
5 - jupyterlab: 0.31.8 -> 0.31.12 [wheel]
6 - Keras: 2.1.2 -> 2.1.5 [wheel]
7 - Markdown: 2.6.10 -> 2.6.11 [wheel]
```

- Executing `python pipupdater.py --install 5 6` will update only packages 5 and 6.
- Exeucting `python pipupdater.py --all` will update everything.
- If the `--log` or `-l` flag is provided, the program will log the output of each update command to a separate file stored in `pipupdatelogs`.
- This utility does not make any assumptions on the path of `pip`, and hence can be used on a `Conda` environment.
