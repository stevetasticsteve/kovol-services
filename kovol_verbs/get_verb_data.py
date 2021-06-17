# This file contains code for pulling elicited verb data from various sources

import csv
from kovol_verbs import KovolVerb


def get_data_from_csv(
    csv_file="kovol_verbs/elicited_verbs.csv", format="object"
) -> list:
    """reads a csv file and outputs a list of KovolVerb objects.
    Can accept 'list' as format to return a list of listed dict entries instead"""
    with open(csv_file, newline="") as file:
        reader = csv.DictReader(
            file, delimiter=",", fieldnames=["actor", "tense", "mode", "kov", "eng"]
        )
        data = [r for r in reader]
        data.pop(0)  # Remove header

    # Get a list of the unique verbs (identified by English translation)
    eng = set([v["eng"] for v in data])
    # Get list of all data where each index is a list of dict items for each translation
    verb_data = [[d for d in data if d["eng"] == e] for e in eng]
    if format == "list":
        return verb_data
    elif format == "object":
        return csv_data_to_verb_object(verb_data)


def csv_data_to_verb_object(verb_data: list) -> list:
    verbs = []
    for d in verb_data:
        eng = d[0]["eng"]  # every row item contains this info
        v = KovolVerb("", eng)  # init obj with temp 1s_future

        future_tense = [v for v in d if v["tense"].lower() == "future"]
        for t in future_tense:
            if t["actor"].lower() == "1s":
                v.future_1s = t["kov"]
            elif t["actor"].lower() == "2s":
                v.future_2s = t["kov"]
            elif t["actor"].lower() == "3s":
                v.future_3s = t["kov"]
            elif t["actor"].lower() == "1p":
                v.future_1p = t["kov"]
            elif t["actor"].lower() == "2p":
                v.future_2p = t["kov"]
            elif t["actor"].lower() == "3p":
                v.future_3p = t["kov"]

        recent_past_tense = [v for v in d if v["tense"].lower() == "recent past"]
        for t in recent_past_tense:
            if t["actor"].lower() == "1s":
                v.recent_past_1s = t["kov"]
            elif t["actor"].lower() == "2s":
                v.recent_past_2s = t["kov"]
            elif t["actor"].lower() == "3s":
                v.recent_past_3s = t["kov"]
            elif t["actor"].lower() == "1p":
                v.recent_past_1p = t["kov"]
            elif t["actor"].lower() == "2p":
                v.recent_past_2p = t["kov"]
            elif t["actor"].lower() == "3p":
                v.recent_past_3p = t["kov"]

        remote_past_tense = [v for v in d if v["tense"].lower() == "remote past"]
        for t in remote_past_tense:
            if t["actor"].lower() == "1s":
                v.remote_past_1s = t["kov"]
            elif t["actor"].lower() == "2s":
                v.remote_past_2s = t["kov"]
            elif t["actor"].lower() == "3s":
                v.remote_past_3s = t["kov"]
            elif t["actor"].lower() == "1p":
                v.remote_past_1p = t["kov"]
            elif t["actor"].lower() == "2p":
                v.remote_past_2p = t["kov"]
            elif t["actor"].lower() == "3p":
                v.remote_past_3p = t["kov"]

        imperatives = [v for v in d if v["mode"]]
        for t in imperatives:
            if t["actor"].lower() == "2s":
                v.singular_imperative = t["kov"]
            elif t["actor"].lower() == "2p":
                v.plural_imperative = t["kov"]
            elif t["mode"].lower() == "short":
                v.short = t["kov"]
        verbs.append(v)

    return verbs


data = get_data_from_csv()
for d in data:
    d.print_paradigm()