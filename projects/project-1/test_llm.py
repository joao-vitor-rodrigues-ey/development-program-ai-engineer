from src.core.llm_client import AzureModel  

llm = AzureModel()
response = llm.invoke("Da um oi pro carlos")
print(response.choices[0].message.content)