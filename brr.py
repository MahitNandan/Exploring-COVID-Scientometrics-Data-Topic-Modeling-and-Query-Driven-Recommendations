import streamlit as st
import pandas as pd
import numpy as np
import json
import tensorflow as tf
import tensorflow_hub as hub

## Load USE model
module_url = "https://tfhub.dev/google/nnlm-en-dim128/2"
embed = hub.KerasLayer(module_url)
# Load embeddings
embeddings_df = pd.read_csv('embeddings.csv')

# Convert embeddings to numpy array
embeddings = embeddings_df.to_numpy()

# Assuming you have 'sent' defined elsewhere in your code
sent = "sent.json"

# Open the JSON file in read mode
with open(sent, "r") as json_file:
    # Load the JSON data
    sent = json.load(json_file)

# Your existing code for similarity calculation and recommendation
# function for recommend text based upon query
    #Calculate cosine similarity of query with all sentences
def cosine_similarity_func(embeddings,embeddings_query):
    '''
    Input:
         embeddings: array or tensor of all sentence embeddings (nX128 for n sentences)
         embeddings_query: array or tensor of query embedding (1X128)
    Output:
         cosine_similarity: cosine similarity of query with each sentence (nX1) 
    '''
    # x.y
    dot_product = np.sum(np.multiply(np.array(embeddings),np.array(embeddings_query)),axis=1)
    
    #||x||.||y||
    prod_sqrt_magnitude = np.multiply(np.sum(np.array(embeddings)**2,axis=1)**0.5, np.sum(np.array(embeddings_query)**2,axis=1)**0.5)
    
    #x.y/(||x||.||y||)
    cosine_similarity  = dot_product/prod_sqrt_magnitude
    return cosine_similarity
def recommended_text(query,embeddings,sent,threshold_min=.95,threshold_max = 1):
    '''
    Input:
         query: list of queries
         embeddings: embeddings of all sentences
         sent:list all sentences
         threshold_min: lower limit of threshold for which sentence is supposed to be similar with query
         threshold_max: upper limit of threshold for which sentence is supposed to be similar with query
         
    Output:
          recommend_text: list of similar sentences with query
    '''
    recommend_text = []
    embeddings_query = embed(query) #create embedding for query
    
    cosine_similarity = cosine_similarity_func(embeddings,embeddings_query) # get cosine similarity with all sentences
    
    # standardize cosine similarity output, Range(0,1)
    standardize_cosine_simi  = (cosine_similarity-min(cosine_similarity))/(max(cosine_similarity)-min(cosine_similarity))
    
    #sort sent based upon cosine similarity score
    sent_prob = list(map(lambda x, y:(x,y), standardize_cosine_simi, sent)) 
    sent_prob.sort(key=lambda tup: tup[0], reverse=True)

    # select sentences by using upper and lower threshold
    for i,j in sent_prob:
        if (i >threshold_min) and (i<=threshold_max):
            recommend_text.append("Similarity: "+str(i)+" Document:"+j)
    return recommend_text  
def main():
    st.title("COVID-19 Research Query Recommendation")
    query = st.text_input("Enter your query here:")
    if st.button("Submit"):
        # Convert the input query into a list containing a single sentence
        query_list = [query]
        # Call your recommended_text function with the input query
        result = recommended_text(query_list, embeddings, sent)
        st.write("Result:", result)

if __name__ == "__main__":
    main()