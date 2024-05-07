from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration
from datasets import load_dataset
import torch
def load_rag_model():
    tokenizer = RagTokenizer.from_pretrained("nklomp/rag-example")
    retriever = RagRetriever.from_pretrained("nklomp/rag-example", dataset=load_dataset("your_dataset"))
    model = RagTokenForGeneration.from_pretrained("nklomp/rag-example", retriever=retriever)
    return tokenizer, model

def query_model(tokenizer, model, query):
    inputs = tokenizer(query, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage
tokenizer, model = load_rag_model()
user_query = "I am looking for companies that can handle a large construction project."
response = query_model(tokenizer, model, user_query)
print(response)


















