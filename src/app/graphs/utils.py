import os
import json
from collections import Counter

from flask import current_app
import pandas as pd

from .. import cache


@cache.memoize(timeout=3600)
def read_logs(day: int = None):
    # print("Calculating read_logs...")
    days = []
    total_status_codes = []
    total_mime_types = []
    with current_app.open_resource(
        os.path.join("static", "network_logs.json")
    ) as logs_file:
        logs = json.loads(logs_file.read())
        status_codes = []
        mime_types = []
        if day:
            logs = logs[day - 1]
            for log in logs["logs"]:

                if "response" in log:
                    status_codes.append(log["response"]["status"])
                    mime_types.append(log["response"]["mimeType"])
            count = len(status_codes) + len(mime_types)

            return count, status_codes, mime_types
        else:
            df = pd.DataFrame()
            for day, log_at in enumerate(logs):

                status_codes = []
                mime_types = []

                for log in log_at["logs"]:

                    if "response" in log:
                        days.append(day)
                        status_codes.append(log["response"]["status"])
                        mime_types.append(log["response"]["mimeType"])
                        total_status_codes.append(log["response"]["status"])
                        total_mime_types.append(log["response"]["mimeType"])

                status_codes_counter = Counter(status_codes)
                mime_types_counter = Counter(mime_types)
                dict_of_lists_mime_by_day = {
                    "day": [day + 1 for _ in range(len(mime_types_counter))],
                    "mime_types": list(mime_types_counter.keys()),
                    "mime_types_count": list(mime_types_counter.values()),
                }
                dict_of_lists_status_by_day = {
                    "day": [day + 1 for _ in range(len(status_codes_counter))],
                    "status_codes": list(status_codes_counter.keys()),
                    "status_codes_count": list(status_codes_counter.values()),
                }
                df = pd.concat(
                    [
                        df,
                        pd.DataFrame(dict_of_lists_mime_by_day),
                        pd.DataFrame(dict_of_lists_status_by_day),
                    ],
                    ignore_index=True,
                )
            count = len(total_status_codes) + len(total_mime_types)
            return count, df
