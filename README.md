# probely-python-homework

## poetry
    https://python-poetry.org/docs/#installation

## install
    make isntall

## apply migrations
    make migrate

## run
    make run

## test
    make test

## Retrieve Findings
    PROBELY_TOKEN={API_TOKEN} \
    PROBELY_TARGET={TARGET_ID} \
    make retrieve_findings

## Retrieve findings from API
    make migrate
    
    make run

    export PROBELY_TOKEN={API_TOKEN}
    export PROBELY_TARGET={TARGET_ID}
    make retrieve_findings

    curl -X GET http://127.0.0.1:8000/api/findings/
