"""Module from elasticsearch subpackage with routes for Elasticsearch features."""

__docformat__ = "google"

import string

import flask
from flask import jsonify, render_template, request, url_for, Blueprint
from elasticsearch import ApiError, TransportError
from elastic_transport import ObjectApiResponse

from .. import es
from ..graphs.utils import read_logs
from .utils import perform_elasticsearch_query

elasticsearch = Blueprint("elasticsearch", __name__)


@elasticsearch.route("/upload")
def upload_documents() -> dict:
    """Upload documents to an Elasticsearch index.

    Returns:
        Empty dictionary.
    """
    _, df = read_logs()

    id = 1
    for day in df["day"].unique():

        doc_in_a_day = df[df["day"] == day].fillna(value=0).to_dict("records")
        for doc in doc_in_a_day:
            # print(id)
            # print(doc)
            try:
                resp = es.index(index="logs-index", id=id, document=doc)
            except ApiError as err:
                print("ApiError")
                print(err.meta.status)
                print(err.meta.headers)
                print(err.body)
                continue
            except TransportError as err:
                print("TransportError")
                print(err)
                continue

            if resp["result"] != "created" or resp["result"] != "updated":
                print(resp["result"])

            id += 1

    return {}


@elasticsearch.route("/search", methods=["POST"])
def search():
    """Return the search results page.

    Returns:
        Rendered template with the search results page.
    """
    hits = search_helper()
    return render_template("query_results.html", hits=hits)


@elasticsearch.route("/api/search", methods=["POST", "GET"])
def api_search() -> flask.Response:
    """Return the search results as a JSON object.

    Query parameters:
        - **query**: query string.\n
        - **day**: 1 if day is to be included in the search results, 0 otherwise.\n
        - **mime_types**: 1 if mime_types is to be included in the search results, 0 otherwise.\n
        - **mime_types_count**: 1 if mime_types_count is to be included in the search results, 0 otherwise.\n
        - **status_codes**: 1 if status_codes is to be included in the search results, 0 otherwise.\n
        - **status_codes_count**: 1 if status_codes_count is to be included in the search results, 0 otherwise.

    Returns:
        JSON object with the search results.

    Examples:
        >>> curl -X GET "http://localhost:5000/api/search?query=39&day=1"
    """
    hits = search_helper()
    for hit in hits:
        if hit["_source"]["mime_types"] != 0.0:
            hit["_source"]["mime_types_count"] = int(hit["_source"]["mime_types_count"])
        if hit["_source"]["status_codes"] != 0.0:
            hit["_source"]["status_codes"] = int(hit["_source"]["status_codes"])
            hit["_source"]["status_codes_count"] = int(
                hit["_source"]["status_codes_count"]
            )
    return jsonify(hits)


@elasticsearch.route("/api/search/<int:id>")
def api_search_by(id: int) -> ObjectApiResponse:
    """Find a document by its ID.

    Args:
        id: document ID

    Returns:
        JSON object with the document.

    Examples:
        >>> curl -X GET "http://localhost:5000/api/search/164"
    """

    try:
        resp = es.get(index="logs-index", id=id)

    except ApiError as err:
        print(err.meta.status)
        print(err.meta.headers)
        print(err.body)
        return jsonify({})

    return resp["_source"]


@elasticsearch.route("/api/delete/<int:id>")
def api_delete_by(id: int) -> flask.Response:
    """Delete a document by its ID.

    Args:
        id: document ID

    Returns:
        Empty JSON object.

    Examples:
        >>> curl -X GET "http://localhost:5000/api/delete/164"
    """
    es.delete(index="logs-index", id=id)
    return jsonify({})


def search_helper():
    """Return the search results based on the request method and query parameters.

    Returns:
        Search results as a list of dictionaries or empty dict or empty list.
    """
    # Get the search query from the form or query parameters, depending on the request method
    if request.method == "POST":

        search_query = request.form["query"]
        fields = []
        if "day" in request.form:
            fields.append("day")
        if "mime_types" in request.form:
            fields.append("mime_types")
        if "mime_types_count" in request.form:
            fields.append("mime_types_count")
        if "status_codes" in request.form:
            fields.append("status_codes")
        if "status_codes_count" in request.form:
            fields.append("status_codes_count")
    elif request.method == "GET":

        search_query = request.args.get("query")
        fields = []
        if "day" in request.args:
            fields.append("day")
        if "mime_types" in request.args:
            fields.append("mime_types")
        if "mime_types_count" in request.args:
            fields.append("mime_types_count")
        if "status_codes" in request.args:
            fields.append("status_codes")
        if "status_codes_count" in request.args:
            fields.append("status_codes_count")

    if search_query is None:
        return {}

    if search_query in string.whitespace:
        return []

    # Call a separate function to perform the Elasticsearch query
    resp = perform_elasticsearch_query(search_query, fields)

    return resp["hits"]["hits"]
