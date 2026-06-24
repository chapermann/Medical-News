from Bio import Entrez

Entrez.email = "system@medicalnews.ai"

def search_pubmed(query, mindate, maxdate):

    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=100,
        datetype="pdat",
        mindate=mindate,
        maxdate=maxdate
    )

    record = Entrez.read(handle)
    return record["IdList"]
