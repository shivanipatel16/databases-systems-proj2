import sys
import tabulate
from googleapi import valid_args, get_url_results
from helper_functions import load_nlp_model, extract_relations
from textprocessing import get_content


def main():
    args = tuple(sys.argv[1:])
    # error message if the arguments are invalid
    if not valid_args(args):
        print("Invalid arguments.")
        print("Usage: python3 retrieval.py <google api key> <google engine id> <r> <t> <q> <k>")
        return

    # parameters
    engine_key, engine_id, relation, target_precision, query, k = args
    target_precision = float(target_precision)
    relation = int(relation)
    k = int(k)

    entities_of_interest = ["ORGANIZATION", "PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]
    subjects_of_interest = objects_of_interest = desired_relation = None

    # matches the desired relation with the corresponding entities of interest
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

    print("----")
    print("Parameters:")
    print("Client key        =", engine_key)
    print("Engine key        =", engine_id)
    print("Relation          =", desired_relation)
    print("Threshold         =", target_precision)
    print("Query             =", query)
    print("# of Tuples       =", k)
    print("----")

    nlp, spanbert = load_nlp_model()

    i = 1
    query_seen = {query} # creates a set of queries we have run to keep track
    urls_seen = set() # creates a set of urls to keep track of the ones we have seen so far
    relations_tuples = dict() # (Subject, Relation, Object) --> Confidence

    while query != None:
        print("\n\n=========== Iteration: {} - Query: {} ===========\n\n".format(i, query))
        urls = get_url_results(query, engine_key, engine_id)

        for a in range(len(urls)):
            url = urls[a]
            print("\nURL ({}/{}): {}".format(a+1, len(urls), url))
            if url in urls_seen:
                print("\tURL has been seen...")
                continue

            urls_seen.add(url)
            text = get_content(url) # calls the function to scrap html files & clean it for spacy
            doc = nlp(text)

            relations = extract_relations(doc, spanbert, desired_relation, entities_of_interest=entities_of_interest, subjects_of_interest=subjects_of_interest, objects_of_interest=objects_of_interest, conf=target_precision)

            for key, value in relations.items():
                if key not in relations_tuples:
                    relations_tuples[key] = value
                elif relations_tuples[key] < relations[key]:
                    relations_tuples[key] = value

        print("================== ALL RELATIONS for {} ( {} ) =================".format(desired_relation, len(relations_tuples)))
        sorted_relations_tuples = list(sum(sorted(relations_tuples.items(), key=lambda x:x[1], reverse=True), ()))
        rows = [[sorted_relations_tuples[k][0], sorted_relations_tuples[k][2], sorted_relations_tuples[k+1]] for k in range(0, len(sorted_relations_tuples), 2)]
        headers = ["Subject", "Object", "Confidence"]
        print(tabulate.tabulate(rows, headers, tablefmt="fancy_grid")) # prints the tuples in a tabular format

        # finds query for next iteration -- based on the highest confidence
        if len(rows) <= k:
            i += 1
            new_query = None
            for r in range(len(rows)):
                t = rows[r]
                q = t[0] + " " + t[1]
                if q not in query_seen:
                    query_seen.add(q)
                    new_query = q
                    break

            query = new_query
            if new_query == None:
                print("ISE has stalled before retrieving k high-confidence tuples.")
                print("Total # of iterations = {}".format(i))
                query = None

        else:
            print("Total # of iterations = {}".format(i))
            break


if __name__ == '__main__':
    main()
