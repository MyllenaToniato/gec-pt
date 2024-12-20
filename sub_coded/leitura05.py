import sys
from lxml import etree
from lxml import html
from nltk.tokenize import sent_tokenize

tree = etree.parse("data/sample_test_frases.xml")
root_xml = tree.getroot()
body = root_xml.find('.//body')
##print(body)

bodyHTML = etree.tostring(body, encoding="unicode", method="html")
# print(bodyHTML)
bodyXML = html.fromstring(bodyHTML)
##print(bodyXML)



tokens = sent_tokenize(bodyXML)

print(tokens)


# for elt in doc.getiterator():
#    print(elt.tag)


# corpo = doc.findtext("body")
# print(corpo)
