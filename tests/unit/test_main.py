import json
import pytest

def test_execute():
    # Opening JSON file
    with open('tests/unit/pullresponse.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)

    print(type(json_object))

    opened = 0
    closed = 0
    in_progress = 0

    print(type(json_object))
    for pull in json_object:
        if pull["state"] == "open":
            opened += 1
        elif pull["state"] == "closed":
            closed += 1
        else:
            in_progress += 1

    print (opened)
    print (closed)
    print (in_progress)
    assert opened == 2 
    assert closed == 28
    assert in_progress == 0