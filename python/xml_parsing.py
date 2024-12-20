"""
Below is code for discovering format / fields in XML data

See also code in `data-sci-snippets\parsing-data\XML` for a complete 
parsing example, once the formats have been defined.

"""

import xml.etree.ElementTree as ET
from collections import defaultdict
import pandas as pd


tree = ET.parse(PATH_TO_XML_FILE)
root = tree.getroot()

# discover child types:
tag_counts = defaultdict(int)
for child in root:
    tag_counts[child.tag] += 1


# examine a child
child = root[0]


## see what kind of attributes the 
for item in child:
    print(item.tag)

child.find(NAME_OF_ONE_TAG).attrib
# > {'display_value': VALUE}

data = []
for item in child:
    # depending on which attributes the child has, you can capture them as follows:
    ## they usually tend to have a `.text` field
    ## `display_value` we discovered from look at tag attributes above
    d = {'tag': item.tag, 'text': item.text, 'display_value': item.attrib.get('display_value')}
    if len (item.attrib) > 1:
        attribs = item.attrib
        del attribs['display_value']
        d['other_attribs'] = attribs
    data.append(d)

child_df = pd.DataFrame.from_dict(data)


## different child tags will tend to have different sub-items/tags, data formats
## e.g. all work notes will have one data structure / set of fields, all attachments another

## Fields can even contain raw bytes for various file types (PDFs, JPGs, etc)
## See more complete XML parsing mentioned above for how to handle