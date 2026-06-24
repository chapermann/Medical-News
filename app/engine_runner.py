from app.services.pubmed import search_pubmed
from app.services.deduplication import filter_new_articles

def run_engine(engine, query, db):

    existing = db.get_pmids(engine.id)

    results = search_pubmed(
        query=query,
        mindate=engine.last_execution,
        maxdate="today"
    )

    new = filter_new_articles(results, existing)

    db.save_articles(new)

    return {
        "total": len(results),
        "new": len(new)
    }
