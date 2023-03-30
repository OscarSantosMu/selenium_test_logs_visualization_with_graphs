from elasticsearch import ApiError, TransportError

from .. import es


def perform_elasticsearch_query(search_query, fields):
    # Create the Elasticsearch query using the search query and fields
    query = {"query": {"multi_match": {"query": search_query, "fields": fields}}}

    try:
        return es.search(index="logs-index", body=query)

    except ApiError as err:
        print(err.meta.status)
        print(err.meta.headers)
        print(err.body)
    except TransportError as err:
        print(err)
