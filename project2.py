import sys

from googleapi import *
from textprocessing import *


def main():
    args = tuple(sys.argv[1:])
    if not valid_args(args):
        print("Invalid arguments.")
        print("Usage: python3 retrieval.py <google api key> <google engine id> as;ldfkj;asldkfj")  # TODO
        return

    key, engine_id, relation, target_precision, query, k = args
    print("----")
    print("Parameters:")
    print("Client key        =", key)
    print("Engine key        =", engine_id)
    print("Relation          =", relation)
    print("Threshold         =", target_precision)
    print("Query             =", query)
    print("# of Tuples       =", k)
    print("----")

    # TODO it says loading necessary libraries. it should take  a minute or so... do we have this to?

    i = 0
    while True:
        print("\n\n=========== Iteration: {} - Query: {} ===========\n\n".format(i, query))

        urls = get_url_results(query, key, engine_id)
        for k in range(len(urls)):
            url = urls[k]
            print("\nURL ({}/{}): {}".format(k, len(urls), url))
            get_content(url)

            # annotate it
            # extract sentences & process 1 by 1

        break

if __name__ == '__main__':
    main()
