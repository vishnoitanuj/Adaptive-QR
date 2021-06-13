import os
import json
from dotenv import load_dotenv
from datetime import datetime
from elasticsearch import Elasticsearch

load_dotenv()
es = Elasticsearch(
        cloud_id=os.environ['CLOUD_ID'],
        http_auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']),
        maxsize=25
    )

class ElasticSearchUtils:

    @staticmethod
    def ingest_data(data, index='test-company'):
        timestamp = datetime.now()
        data['lastUpdated'] = timestamp.strftime('%m/%d/%Y')
        try:
            res = es.index(index=index, body=data)
            if not res['result']=='created':
                raise Exception('Creation failed for data '+data)
            print("Data successfully ingested")
        except Exception as e:
            print(str(e))
    
    @staticmethod
    def get_data(query_data, index='test-company'):
        shouldQuery = []
        [shouldQuery.append({'term': {k : v} }) for k,v in query_data.items()]
        query = json.dumps({'query': {'bool': {'should': shouldQuery, "minimum_should_match": 1}}})
        print(query)
        res = es.search(
            index=index, 
            body=query
            )
        result_data = list()
        for result in res['hits']['hits']:
            result_data.append(result['_source'])
        return result_data