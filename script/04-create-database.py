"""
Script to initialize a mongo database (named 'data') and collection (named 'urls')
via pymongo
"""
import pymongo


def main():
    print("Connecting to database")
    client = pymongo.MongoClient()
    print("Creating database 'data'")
    db = client.data
    print("Creating collection 'urls' with ascending index on short_url")
    urls = db.urls
    urls.create_index([("short_url", pymongo.ASCENDING)], unique=True)


if __name__ == '__main__':
    main()
