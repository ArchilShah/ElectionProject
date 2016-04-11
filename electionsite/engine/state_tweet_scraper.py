import db_utils
import auth
import time
import sys

api = auth.get_api()
with open('candidates.txt', 'r') as f:
    candidates = f.read().split('\n')

with open('states.csv', 'r') as f:
    states_raw = f.read().split('\n')
    states = dict()
    for state_line in states_raw:
        state_arr = state_line.split(',')
        state_data = {
            "name": state_arr[0],
            "longitude": state_arr[1],
            "latitude": state_arr[2],
            "radius": state_arr[3]
        }
        states[state_data["name"]] = state_data

def search_candidate_in_state(candidate, state_name):
    state = states[state_name]
    coordinates = state['longitude'] + ',' + state['latitude']
    queryTerms = {"q":candidate,"geocode":coordinates + "," + state['radius'] + "km", "count":100}
    query = api.request('search/tweets',queryTerms).json()

    if 'errors' in query:
        if query['errors'][0]['code'] == 88:
            print "Rate limit exceded; trying again in 5 minutes"
            time.sleep(5 * 60)
        else:
            print "Unknown Error: " + str(query)
            sys.exit(1)
    
    # Mark each tweet with the state recorded in
    for tweet in query['statuses']:
        tweet['state'] = state['name']
        tweet['candidate'] = candidate

    print """Found {2} tweets while searching for {0} in {1}""".format(candidate, state_name, len(query['statuses']))
    return query['statuses']

def country_wide_search_on_candidate(candidate):
    tweets = list()
    for state in states:
        tweets = search_candidate_in_state(candidate, state)
        for t in tweets:
            db_utils.save_to_database(t)

if __name__ == "__main__":
    for candidate in candidates:
        country_wide_search_on_candidate(candidate)
