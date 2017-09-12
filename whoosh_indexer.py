import os
import whoosh
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

##Schema definition, stores every field except content
##All fields except path are searchable
schema = Schema(path=ID(stored=True),
                journal=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                authors=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                affiliations=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                body=TEXT(analyzer=StemmingAnalyzer())
                )

##Create the index
def createIndex(indexDir,schema):
    if not os.path.exists(indexDir):
        os.mkdir(indexDir)
    ix = index.create_in(indexDir, schema, indexname="PubMedIdx")
    return ix

##Open the index if it exists, if not, create it
def openIndex(indexDir,schema):
    if  index.exists_in(indexDir, indexname="PubMedIdx"):
        ix = index.open_dir(indexDir, indexname="PubMedIdx")
    else:
        ix = createIndex(indexDir,schema)
    return ix

##NOT USED: Slower than ETIndexPubmedXML
def soupIndexPubmedXML(XMLfile,ix):
    absPath = os.path.abspath(XMLfile)
    writer = ix.writer()
    soup = BeautifulSoup(open(XMLfile), 'lxml')
    for article in soup.find_all('article'):
        journalTitle = article.find('journal-title').text
        articleTitle = article.find('article-title').text
        contributors = ""    
        for contrib in article.find_all("contrib"):
            firstName = contrib.find("name").find("given-names").text
            lastName = contrib.find("name").surname.text
            contribName = firstName + " " + lastName
            contributors += contribName + ","
        affiliations = []
        for aff in article.find_all("aff"):
            affiliations.append(aff.text)
        try:
            content = article.find("abstract").text
            for sec in article.find_all("sec"):
                content += sec.text
        except:
            print "Could not find article content in " + XMLfile
            content = ""
        writer.add_document(path=unicode(absPath),
                            journal=unicode(journalTitle),
                            title=unicode(articleTitle),
                            authors=unicode(contributors),
                            affiliations=unicode(str(affiliations)),
                            body=unicode(content))
        writer.commit()

##For each article in XMLfile
##Get journal title, article title, authors, affiliations and content
##Add those fields to the index along with the file path
def ETIndexPubmedXML(XMLfile,ix):
    writer = ix.writer()
    try:
        absPath = os.path.abspath(XMLfile)
        tree = ET.parse(XMLfile)
        root = tree.getroot()
        affiliations = []
        contributors = ""
        content = ""
        for el in root.iter():
            if el.tag == 'journal-title':
                journalTitle = el.text
            elif el.tag == 'title-group':
                articleTag = el.find('article-title')
                articleTitle = "".join(articleTag.itertext())
            elif el.tag == 'contrib':
                nameTag = el.find("name")
                try:
                    firstName = nameTag.find("given-names").text
                except:
                    firstName = ""
                try:
                    lastName = nameTag.find("surname").text
                except:
                    lastName = ""
                try:
                    contribName = firstName + " " + lastName
                except:
                    contribName = ""
                contributors += contribName + ","
            elif el.tag == 'aff':
                affiliations.append("".join(el.itertext()))
            elif el.tag == 'abstract':
                content = "".join(el.itertext())
            elif el.tag == "sec":
                content += "".join(el.itertext())
        writer.add_document(path=unicode(absPath),
                                journal=unicode(journalTitle),
                                title=unicode(articleTitle),
                                authors=unicode(contributors),
                                affiliations=unicode(str(affiliations)),
                                body=unicode(content))
        writer.commit()
    except:
        writer.cancel()
        
def searchIndex(term,ix):
    s = ix.searcher()    
    qp = whoosh.qparser.MultifieldParser(["title", "journal", "authors", "affiliations", "body"], ix.schema)
    q = qp.parse(unicode(term))
    results = s.search(q,terms=True)    
    for hit in results:
        print hit
        print(hit.matched_terms())

ix = openIndex("/home/mfeltz/workdir/PubMedIdx",schema)
##Loop through pubmed XMLs
for path, dirs, files in os.walk("/mnt/Passport1/pubmed/O-Z_XML/"):
    dirPath = path + '/'
    for file in files:
        (root, ext) = os.path.splitext(file)
        try:
            if ext == ".nxml" or ext == ".xml":
                print file
                ETIndexPubmedXML(dirPath + file,ix)
        except NameError:
            print "No filename to split"
