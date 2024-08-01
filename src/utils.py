from langchain_community.chat_models import ChatOpenAI
def create_openai_chat(api_key, model, temperature):
    model = ChatOpenAI(
        api_key = api_key, 
        model = model, 
        temperature =temperature
        )
    return model