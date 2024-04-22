
from piazza_api import Piazza

p = Piazza()
p.user_login() 
course = p.network("lhjo3qc1jfn1e1")
response = p._rpc_api.request(method="network.filter_feed",
                              data={"nid":"lhjo3qc1jfn1e1","unresolved":1},                              
                              api_type="logic",
                              
                              )
if 'result' in response:

    feed = response['result']['feed']

    unanswered_post_ids = []
    for post in feed:
        if post['no_answer'] == 1:
            unanswered_post_ids.append(post['nr'])

    print("Unanswered Post IDs:")
    print(unanswered_post_ids)
else:
    print("Error fetching feed:", response['error'])