# IMPORT from Core libraries
import os
import uuid
# IMPORT from External libraries
from qdrant_client import QdrantClient, models
# IMPORT from Internal libraries
from lib.mistral.utils import get_text_embedding

qdrant_client = QdrantClient(
    url=os.environ.get('QDRANT_HOST'),
    api_key=os.environ.get('QDRANT_API_KEY'),
)

def get_relevant_points( query ):
    results = qdrant_client.search(
        collection_name='mistral',
        query_vector=get_text_embedding( query ),
    )
    return results

def get_point_from_chunk( chunk ):
    id = str(uuid.uuid4())
    embedding = get_text_embedding( chunk )
    point = models.PointStruct(id=id, payload= {"content" : chunk}, vector=embedding)
    return point

def upload_points( points ):
    qdrant_client.upsert(
        collection_name='mistral',
        points=points
    )