import json
import string
from datetime import datetime

from flask import jsonify, render_template, request, Blueprint
from elasticsearch import ApiError, TransportError

from .. import es
from ..main.utils import read_logs

elasticsearch = Blueprint("elasticsearch", __name__)


@elasticsearch.route("/upload")
def upload_documents():

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


@elasticsearch.route("/api/search", methods=["POST", "GET"])
@elasticsearch.route("/search", methods=["POST"])
def search():
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
        return jsonify({})
    elif search_query in string.whitespace:
        return render_template("query_results.html", hits=[])

    # Call a separate function to perform the Elasticsearch query
    resp = perform_elasticsearch_query(search_query, fields)

    if request.path.startswith("/api"):
        # If the request is for the API endpoint, return the search results as JSON
        for hit in resp["hits"]["hits"]:
            if hit["_source"]["mime_types"] != 0.0:
                hit["_source"]["mime_types_count"] = int(
                    hit["_source"]["mime_types_count"]
                )
            if hit["_source"]["status_codes"] != 0.0:
                hit["_source"]["status_codes"] = int(hit["_source"]["status_codes"])
                hit["_source"]["status_codes_count"] = int(
                    hit["_source"]["status_codes_count"]
                )
        return jsonify(resp["hits"]["hits"])
    else:
        # If the request is for the regular endpoint, render the search results as HTML
        return render_template("query_results.html", hits=resp["hits"]["hits"])


@elasticsearch.route("/api/search/<int:id>")
def api_search_by(id: int):

    try:
        resp = es.get(index="logs-index", id=id)

    except ApiError as err:
        print(err.meta.status)
        print(err.meta.headers)
        print(err.body)
        return jsonify({})

    return resp["_source"]


@elasticsearch.route("/api/delete/<int:id>")
def api_delete_by(id: int):

    es.delete(index="logs-index", id=id)
    return jsonify({})


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
