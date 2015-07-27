import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError as ETParseError


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
            text = subel.attrib.get(attribute)
        else:
            text = subel.text
        if text is None:
            text = default
        elif convert:
            try:
                text = convert(text)
            except:
                if quiet:
                    text = default
                else:
                    raise
        result += [text]
    return result if multi else result[0]
