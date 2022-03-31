from googleapiclient.discovery import build


def valid_args(args):
    """
    TODO: documentation
    returns whether args are valid and can process a call to the search engine
    checks for:
        (1) number of command line args
        (2) target precision is a float between 0 and 1
        (3) can successfully query first result using key and engine_id provided
    :param args: command line args as a tuple of strings
    :return: boolean True or False on whether the args given are valid or not
    """

    # python3 project2.py <google api key> <google engine id> <r> <t> <q> <k>
    if len(args) != 6:
        return False

    key, engine_id, relation, target_precision, query, k = args

    try:
        # TODO: more error checking the arguments
        # if float(target_precision) > 1 or float(target_precision) < 0:
        #     return False
        r = try_connection(query, key, engine_id)
        return True
    except:
        return False


def try_connection(query, key, engine_id):
    """
    function created to test connection using key and engine ID for Google Search API
    :param query: string that contains 1 or more words
    :param key: Google Custom Search Engine JSON API Key
    :param engine_id: Engine ID
    :return: result of query
    """
    service = build("customsearch", "v1",
                    developerKey=key)
    return service.cse().list(
        q=query,
        cx=engine_id,
    ).execute()


def get_url_results(query, key, engine_id):
    """
    makes a call to the Google search engine api to find top 10 results for given query
    if non-html file, file is not returned in user_res[0]
    :param key: Google Custom Search Engine JSON API Key
    :param engine_id: Engine ID
    :param query: string that contains 1 or more words
    :return: list of urls
    """
    service = build("customsearch", "v1",
                    developerKey=key)

    res = service.cse().list(
        q=query,
        cx=engine_id,
    ).execute()

    if "items" not in res:
        return None, 0

    results = list()
    for result in res["items"]:
        if "fileFormat" in result:
            continue

        results.append(result["formattedUrl"])

    return results
