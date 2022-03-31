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
    relation = int(relation)

    print("----")
    print("Parameters:")
    print("Client key        =", key)
    print("Engine key        =", engine_id)
    print("Relation          =", relation)
    print("Threshold         =", target_precision)
    print("Query             =", query)
    print("# of Tuples       =", k)
    print("----")

    entities_of_interest = ["ORGANIZATION", "PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]
    subjects_of_interest = objects_of_interest = None

    if relation == 1:
        entities_of_interest = ["PERSON", "ORGANIZATION"]
        desired_relation = "per:schools_attended"
    elif relation == 2:
        entities_of_interest = ["PERSON", "ORGANIZATION"]
        desired_relation = "per:employee_of"
    elif relation == 3:
        entities_of_interest = ["PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]
        desired_relation = "per:cities_of_residence"
    elif relation == 4:
        entities_of_interest = ["ORGANIZATION", "PERSON"]
        desired_relation = "org:top_members/employees"
    if 1 <= relation <= 4:
        subjects_of_interest = entities_of_interest[:1]
        objects_of_interest = entities_of_interest[1:]

    nlp, spanbert = load_nlp_model()

    i = 0
    urls_seen = set()

    while True:
        print("\n\n=========== Iteration: {} - Query: {} ===========\n\n".format(i, query))

        urls = get_url_results(query, key, engine_id)

        for k in range(len(urls)):
            url = urls[k]
            print("\nURL ({}/{}): {}".format(k, len(urls), url))
            if url in urls_seen:
                print("\tURL has been seen...")
                continue

            urls_seen.add(url)
            text = get_content(url)
            doc = nlp(text)

            relations = extract_relations(doc, spanbert, desired_relation, entities_of_interest=entities_of_interest, subjects_of_interest=subjects_of_interest, objects_of_interest=objects_of_interest, conf=target_precision)
            # TODO: readme

            print("Relations: {}".format(dict(relations)))

            # get the relevant tuples with high enough predictions
            # check it against the previous ones we have
            # see if we have enough ones
            # if not, continue searching by getting a new query through the top extraction

        break  # TODO: correct break condition


if __name__ == '__main__':
    main()