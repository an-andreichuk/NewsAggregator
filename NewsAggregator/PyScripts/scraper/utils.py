# -*- coding: utf-8 -*- 
import re


def get_checked_news(collection):
    res = []
    query_response = collection.find({}, {'SourceUrl': 1, '_id': 0})
    for x in query_response:
        res.append(x['SourceUrl'])
    return res


def normalize(text_strings):
    """
    Normalizes text strings which start/end with the following symbols: ':', '.', ',' quotes or whitespace.
    For example, concatenates next line, that starts with comma. with previous line
    or concatenates previous line, that ends with whitespace, with next line.
    :param text_strings: list of strings to be normalized
    :return: list of normalized strings
    """
    joined = "Δ".join(text_strings)
    joined = re.sub("\t\t+", " ", joined)
    joined = re.sub("\\s\\s+", " ", joined)
    joined = re.sub("(Δ)*(,)(Δ)*", r"\2", joined)
    joined = re.sub("(Δ)*(:)(Δ)*", r"\2", joined)
    joined = re.sub('(Δ)*(")(Δ)*', r"\2", joined)
    joined = re.sub("(Δ)*(«)(Δ)*", r"\2", joined)
    joined = re.sub("(Δ)*(»)(Δ)*", r"\2", joined)
    joined = re.sub("(Δ)*(“)(Δ)*", r"\2", joined)
    joined = re.sub("(Δ)*(”)(Δ)*", r"\2", joined)
    joined = re.sub("(Δ)(.)(Δ)", r"\2\n", joined)
    joined = re.sub("Δ\s", " ", joined)
    joined = re.sub("\sΔ", " ", joined)
    joined = re.sub("Δ", "\n", joined)
    splited = joined.split("\n")
    final = [line for line in [x.strip() for x in splited if x] if line]
    return final
