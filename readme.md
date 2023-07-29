## LambdaTest Challenge

## Test Logs Visualization with Graphs
As a company, I run ~2 Million Selenium test Network logs a day on cloud. Build an ability to graphically visualize the logs using a low end resource cloud architecture framework. This code should be able to package and run on self-hosted machines or on cloud with proxy settings and public APIs for subscribed customers. 


## Required for this challenge

What I did:

- [x] Setup Selenium on my local machine.
- [x] Wrote a script to open the URL https://www.lambdatest.com/
- [x] Click on each header navigation items.
- [x] Stored the network logs generated on the browser to my local machine.
- [x] Repeated the process for more than 100 tests.
- [x] Used a lightweight graph library to render a time series of 365 days on the x-axis and y-axis with the following metrics:
    - [x] Total count of logs.
    - [x] Logs count/average stacked by log type (mime-type).
    - [x] Logs count/average stacked by log level (Status Codes).
    - [x] Logs should be able to filter on the UI by any available key-value.
    - [x] Logs should be searchable with a keyword using an API to fetch the results.
- [x] Used the GitHub Flow when working on the task (PRs and issues were made in a different private repo)
- [x] Packaged the code and can run on self-hosted machines or on cloud with proxy settings and public APIs for subscribed customers.

## Bonus

What I added:

- [x] Automated log storage
This allowed me to run the selenium script whenever I wanted without worrying about existing logs and not not overloading the lambdatest server with my requests or incurring in request limit rates.

    Where?
        - [generate-logs.py](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/e01b5164c287fccf19e9ac8fd242137656715bf1/src/scripts/generate-logs.py#L45)
        - [execute-script.py](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/main/src/scripts/execute-script.py)

- [x] Built a dashboard with bar charts specific to each day
This is helpful for a user that wants to see the a query filtered by day in a chart.

    Where?
        - [graphs/routes.py](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/e01b5164c287fccf19e9ac8fd242137656715bf1/src/app/graphs/routes.py#L58)

- [x] Added caching to improve performance by preventing the file being loaded to memory for each request

    Where?
        - [app/__init__.py](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/e01b5164c287fccf19e9ac8fd242137656715bf1/src/app/__init__.py#L29)
        - [graphs/utils.py](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/e01b5164c287fccf19e9ac8fd242137656715bf1/src/app/graphs/utils.py#L15)


- [x] Created an API to handle CRUD operations with an Elasticsearch index
This allowed me to easily upload and interact with the logs and make changes to them as needed.

    Where?
        - [elasticsearch/routes.py](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/main/src/app/elasticsearch/routes.py)

- [x] Added tests that cover some endpoints and created a CI pipeline for them

    Where?
        - [tests_utils.py](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/main/tests/test_utils.py)
        - [test_app.py](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/main/tests/test_app.py)
        - [test.yml](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/main/.github/workflows/test.yml)


- [x] Generated auto-generated self-hosted docs
This is helpful for users to understand how to interact with the API, the routes and access the logs.

    Where?
        - Everywhere 😀

    <sub>Windows</sub>
    ```console
    python -m venv env
    env\Scripts\activate
    pip install -r requirements.txt
    cd src && pdoc app
    ```


## Demo

### App

https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/assets/38818848/313f73b5-50a2-4c86-a4bb-cd73d2b7ef13

### Docs and API

https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/assets/38818848/38fdbf60-7955-496d-999a-b3222b5e4d47

## Getting started

1. [Clone the code repository](#clone-the-code-repository)
2. [Setup a Python virtual environment](#setup-a-python-virtual-environment)
3. [What is missing in the repo to try the app?](#what-is-missing-in-the-repo-to-try-the-app)
    1. [Steps for network_logs.json](#steps-for-network_logsjson)
    2. [Steps for .env](#steps-for-env)
4. [Install and Setup Elasticsearch](#install-and-setup-elasticsearch)
5. [Run the app](#run-the-app)

### Clone the code repository

```console
git clone https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs.git
```
```console
cd selenium_test_logs_visualization_with_graphs
```

### Setup a Python virtual environment

```console
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

### What is missing in the repo to try the app?

1. network_logs.json
2. .env

network_logs.json \- There are [size limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github). To track files beyond this limit, you must use Git Large File Storage [(Git LFS)](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage). But network_logs.json is generated by the code and it makes no sense to add it with Git LFS. 

.env \- should be added since the code gets some environment variables from it.


#### Steps for network_logs.json

Run either generate-logs.py or execute-script.py

[generate-logs.py](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/main/src/scripts/generate-logs.py) will generate a single run. It will create the file if it does not exist or append<sup>1</sup> data to the file if it does exist.
> <sup>1</sup> despite the code overrides the file with a write mode operation it actually apends at the end because of the code logic.

[execute-script.py](https://github.com/OscarSantosMu/selenium_test_logs_visualization_with_graphs/blob/main/src/scripts/execute-script.py) by default will repeat the process 100 times and it will take between 1-2 hours depending on your system, because in addition to waiting the specified time in sleep function, it will take time for the script to save the *large file*<sup>2</sup> to the disk.
> <sup>2</sup> For me it was 807 MB

#### Steps for .env

Create the .env file and add your environment variables
```
HOST=localhost
ELASTIC_PASSWORD="the password you got from bin\elasticsearch.bat"
CA_CERTS_PATH=C:\path_to_your_elasticsearch_folder\config\certs\http_ca.crt
```

### Install and Setup Elasticsearch

1. [Install](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
2. [Setup](https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-stack-security.html)

### Run the app

```py
cd src
python run.py
```

## Notes

1. I found better to assign each run\_id of 100 to a day in the time-series graph since the dashboard shows my features better than it would by using the timestamps of a single day and displaying all logs in a time-series of 365 days.

## Potential improvements outside of this assignment scope.

1. Modify code logic to use append mode operation to avoid loading a big file and then writing again from scratch.
2. Save the file to a remote cloud storage system and retrieve logs with a NoSQL Database.
3. UI/UX.
4. Separate API from server and add swagger-based documentation for it.
5. Performance.
6. Move elasticsearch to managed cloud-hosted cluster.
7. Deploy docs.


