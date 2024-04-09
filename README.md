# makemap
This Python script updates the HTML imagemap generated by FreeMind to remove the reference table and cause the leaf links to point directly to their remote websites.

The is needed as:

1. FreeMind's Export to HTML Clickable Image option adds an unnecessary table below the image map containin the actual links to the remote websites.
2. The imagemap is centered rather than left justified.
3. A link needs to be added to return the user to the home page.

## Usage:
```
$ python makemap.py [-d] filename
```

## Example:
```
$ python makemap.py MyMap.html
FreeMind MakeMap Utility V1.0, processing MyMap.html...
FMID_1097832583FM => https://toydip.com/collections/meccano
<area shape="rect" href="https://toydip.com/collections/meccano" alt="" title="" coords="684,436,862,490" />
```

### Notes
This will create 2 additional files using the following naming covention:
1. filename-without-extension**-temp**.html
2. filename-without-extension**-reduced**.html
