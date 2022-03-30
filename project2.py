import sys
from googleapi import *
from spacy_help_functions import load_nlp_model
from textprocessing import *
from spacy_help_functions import extract_relations


def main():
    args = tuple(sys.argv[1:])
    if not valid_args(args):
        print("Invalid arguments.")
        print("Usage: python3 retrieval.py <google api key> <google engine id> as;ldfkj;asldkfj")  # TODO
        return

    key, engine_id, relation, target_precision, query, k = args
    target_precision = float(target_precision)

    print("----")
    print("Parameters:")
    print("Client key        =", key)
    print("Engine key        =", engine_id)
    print("Relation          =", relation)
    print("Threshold         =", target_precision)
    print("Query             =", query)
    print("# of Tuples       =", k)
    print("----")

    nlp, spanbert = load_nlp_model()

    i = 0
    urls_seen = set()
    while True:
        print("\n\n=========== Iteration: {} - Query: {} ===========\n\n".format(i, query))

        urls = get_url_results(query, key, engine_id)
        entities_of_interest = ["ORGANIZATION", "PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]

        for k in range(len(urls)):
            url = urls[k]
            print("\nURL ({}/{}): {}".format(k, len(urls), url))
            if url in urls_seen:
                print("\tURL has been seen...")
                continue

            urls_seen.add(url)
            text = get_content(url)
            print(text)
            # text = "Bill Gates stepped down as chairman of Microsoft in February 2014 and assumed a new post as technology adviser to support the newly appointed CEO Satya Nadella. Microsoft is an amazing company owned by Bill Gates."

            doc = nlp(text) # TODO

            relations = extract_relations(doc, spanbert, entities_of_interest, conf=target_precision) # TODO: need to make sure it only does entities that matter for the relation

            print("Relations: {}".format(dict(relations)))
            print(doc)

            # get the relevant tuples with high enough predictions
            # check it against the previous ones we have
            # see if we have enough ones
            # if not, continue searching by getting a new query through the top extraction

        break  # TODO: correct break condition


if __name__ == '__main__':
    main()
