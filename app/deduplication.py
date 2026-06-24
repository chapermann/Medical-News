def filter_new_articles(pmids, existing_pmids):

    return list(set(pmids) - set(existing_pmids))
