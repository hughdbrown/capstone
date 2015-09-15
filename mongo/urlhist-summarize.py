from collections import Counter

import simplejson
from pymongo import MongoClient

client = MongoClient()
db = client.data
items = list(db.urlhist.find({}, {'timestamp': 1, 'country': 1, '_id': 0}))

# >>> sum(1 for d in items if "country" not in d)
# 10751

c = Counter(
    (d["timestamp"].day, d["timestamp"].hour, d["timestamp"].minute, d["country"])
    for d in items if "country" in d
)
t = [
    {'day': day, 'hour': hour, 'minute': minute, 'country': country, 'count': count}
    for (day, hour, minute, country), count in c.items()
]
with open("urlhist-timestamp-country.json", "w") as f:
    f.write(simplejson.dumps(t))

c = Counter(
    (d["timestamp"].day, d["timestamp"].hour, d["timestamp"].minute)
    for d in items
)
t = [
    {'day': day, 'hour': hour, 'minute': minute, 'count': count}
    for (day, hour, minute), count in c.items()
]
with open("urlhist-timestamp.json", "w") as f:
    f.write(simplejson.dumps(t))
