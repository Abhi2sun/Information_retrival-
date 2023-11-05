import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

indexName="news"

try:
    es =  Elasticsearch(['http://localhost:9200/'], http_auth=('elastic', 'xxxx'))
except ConnectionError as e:
    print("ConnectionError:",e)

if es.ping():
    print("successfully connected to elasticsearch")
else:
    print("Not successfully connected to elasticsearch")

def search(input_keyword):
    model=SentenceTransformer("all-mpnet-base-v2")
    input_vector=model.encode(input_keyword)
    query={
    "field":"content_vector",
    "query_vector":input_vector,
    "k":5,
    "num_candidates":500,
    }
    res=es.knn_search(index="news",knn=query,source=["title","content","category"])
    results=res["hits"]["hits"]
    return results

def main():
    st.title("Search & Scroll BBC News")
    search_query=st.text_input("Enter your search query")
    if st.button("search"):
        if search_query:
            results=search(search_query)

            st.subheader("Search Results")
            for result in results:
                with st.container():
                    if '_source' in result:
                        try:
                            st.header(f"{result['_source']['title']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"content:{result['_source']['content']}")
                            st.write(f"score:{result['_score']*100}%") 
                        except Exception as e:
                            print(e)
                        st.divider()

if __name__=="__main__":
    main()


