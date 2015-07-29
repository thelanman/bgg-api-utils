import time
import random

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError as ETParseError


class Throttle(object):
    def __init__(self, sleep):
        self.sleep = sleep

    def __call__(self, f):
        def do_throttle(*args, **kwargs):
            time.sleep(random.randint(*self.sleep))
            return f(*args, **kwargs)
        return do_throttle


def load_xml_from_file(fn):
    with open(fn, 'r') as f:
        return ET.fromstring(f.read())


def get_xml_subelement(xml_elem, subelement, attribute=None, multi=False, convert=None, default=None, quiet=False):
    """
    Return the text or attribute of the specified subelement

    === PARAMETERS ===
    xml_elem  : search the children nodes of this element
    subelement: name of the subelement whose text will be retrieved
    attribute :
    convert   : if not None, a callable used to perform the conversion of the text to a certain object type
    default   : default value if subelement is not found
    quiet     : if True, don't raise exceptions from conversions, instead use the default value

    === RETURN ===
    The text associated with the sub-element or ``None`` in case of error

    === EXAMPLE ===
    <xml_elem>
        <subelement value="THIS1">text1</subelement>
        <subelement value="THIS2">text2</subelement>
    </xml_elem>

    >>> get_xml_subelement(xml_elem, 'subelement')
    text1
    >>> get_xml_subelement(xml_elem, 'subelement', value')
    THIS1
    >>> get_xml_subelement(xml_elem, 'subelement', value', True)
    [THIS1, THIS2]
    """
    if xml_elem is None or not subelement:
        return None
    subel = xml_elem.findall(subelement)
    if len(subel) == 0:
        return [default] if multi else default
    result = []
    for el in subel:
        text = None
        if attribute is not None:
            if type(attribute) is list:
                text = []
                for a in attribute:
                    text += [el.attrib.get(a)]
            else:
                text = el.attrib.get(attribute, default)
        else:
            text = el.text if el.text is not None else default
        if convert:
            try:
                text = convert(text)
            except:
                if quiet:
                    text = default
                else:
                    raise
        result += [text]
    return result if multi else result[0]
