#-------------------------------------------------------------------------------
#      Name:  makemap.py
#   Purpose:  Read an HTML image map file from FreeMind and flatten the map.
#             This removes the list generated by FreeMind at the bottom of the
#             HTML page and puts the links directly into the map.
#
#    Author:  Mike Smith
#
#   Created:  06/04/24 - Initial version.
#  Modified:  10/04/24 - Only write map links that resolve to remote sites.
# Copyright:  (c) Mike 2024
#-------------------------------------------------------------------------------
import argparse

# Variables.
version = 'V1.0'

# Parse the input file.
# Check for any command line args.
parser = argparse.ArgumentParser(description='This program reads an exported FreeMind HTML image map and resolves and removes the unnecessary reference table.')
parser.add_argument('filename', help='input file, the exported HTML image map, for example MyMap.html')
parser.add_argument('-d', '--debug', help='print some debugging output', action='store_true')
args = parser.parse_args()
debug = args.debug
filename = args.filename
print(filename)

root = filename[0:filename.find('.')]
if debug:
    print(root)
inp_file = root + '.html'
tmp_file = root + '-temp.html'
out_file = root + '-reduced.html'

# Now run.
print(f'FreeMind MakeMap Utility {version}, processing {filename}...')

# Read the input file into memory, putting all map anchors into a hashmap.
with open(inp_file, 'r') as reader:
    lines = reader.readlines()

# Open a temporary output file.
tmp = open(tmp_file, 'w')

# Now read whole map and replace the local hrefs with remote ones.
for line in lines:
    ln = line.strip()

    # Add in some linefeeds for easier parsing and debugging.
    ln = ln.replace("</head>", "\n<head>\n")
    ln = ln.replace("<body>", "<body>\n")
    ln = ln.replace("</h1>", "</h1>\n")
    ln = ln.replace("</div>", "</div>\n")
    ln = ln.replace("</map>", "</map>\n")
    ln = ln.replace(" />", " />\n")

    if debug:
        print(ln)
    tmp.write(ln)

# Close the temporary file.
tmp.close()

# Now open the temp file to build a hashmap of links.
with open(tmp_file, 'r') as reader:
    lines = reader.readlines()

# Process the temp file, to build a map of links.
inlink = False
link_map = {}
for line in lines:
    ln = line.strip()

    # if line begins with <a id=...> then look for the remote link.
    if ln.startswith('<a id='):
        if debug:
            print(ln)
        k = ln[7:]
        eidx = k.find('FM\"')
        k = k[0:eidx+2]
        if debug:
            print(k)
        inlink = True
    if inlink:
        if 'href=' in ln:
            v = ln
            inlink = False

            # Extract the link e.g. <a href="https://www.meccanospares.com/">Meccano Spares</a>
            sidx = v.find('<a href=')
            lnk = v[sidx+9:]
            eidx = lnk.find('\">')
            lnk = lnk[0:eidx]

            # Put the remote link address in the map.
            link_map[k] = lnk

# Check the map.
for k,v in link_map.items():
    print(f'{k} => {v}')

# Process the temp file again, to write the reduced output.
out = open(out_file, 'w')

for line in lines:
    ln = line.strip()
    if debug:
        print(ln)

    # Only output an href if it points to a remote site.
    write_link = True;
    if '#FMID_' in ln:
        sidx = ln.find('FMID_')
        eidx = ln.find('FM\"')
        k = ln[sidx:eidx+2]
        # Resolve the local anchor to a remote link.
        if k in link_map.keys():
            v = link_map[k]
            if debug:
                print(f'{k} anchor in dictionary, replacing with {v}')
            ln = ln.replace("#" + k, v)
            print(ln)
        else:
            if 'fm_imagemap' not in ln:
                write_link = False

    if write_link:
        out.write(ln + '\n')

    # Stop processing at the end of the map.
    if ln.endswith('</map>'):
        out.write('<div id=\"footer\">\n')
        out.write('&copy; Mike Smith - 2024 Melbourne, Australia <a href="https://www.solveitsmarter.com">solveitsmarter.com</a>\n')
        out.write('</div>\n')
        out.write('</body>\n')
        out.write('</html>\n')
        break

# Close the output file.
out.close()
