from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from app.database.mongo import db
from app.schemas.chat_schema import ChatSessionCreate, ChatSessionResponse
from app.auth.jwt_auth import JWTBearer
from app.schemas.user_schema import UserSchema
from app.auth.dependencies import get_current_user_from_token
from langchain_chroma import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# loader = PyPDFLoader("app/assets/Bezos.pdf")
# docs = loader.load_and_split()
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)
# embeddings = OpenAIEmbeddings()
# chroma_db = Chroma.from_documents(
#     documents=docs, 
#     embedding=embeddings, 
#     persist_directory="data", 
#     collection_name="capstone"
# )

router = APIRouter()
@router.post("/chat/session", response_model=ChatSessionResponse, dependencies=[Depends(JWTBearer())])
async def create_chat_session(session: ChatSessionCreate, user: UserSchema = Depends(get_current_user_from_token)):
    now = datetime.now(timezone.utc)
    session_dict = session.model_dump()
    query = session_dict["content"]

    chroma_db = Chroma(
    persist_directory="data",
    embedding_function=OpenAIEmbeddings(),
    collection_name="capstone"
    )

    # Embed query and get relevant context
    source_docs = chroma_db.similarity_search(query=query)
    context = "\n".join([doc.page_content for doc in source_docs])

    # Retrieve or initialize session
    existing_session = await db["chat_sessions"].find_one({"user_id": user.id})

    chat_history = []
    if existing_session:
        for msg in existing_session.get("messages", []):
            if msg["sender"].lower() == "human":
                chat_history.append(HumanMessage(content=msg["content"]))
            else:
                chat_history.append(AIMessage(content=msg["content"]))

    # Build and send prompt to LLM
    prompt = """
    Answer the user query based on the context and analyze the chat history when required.
    If the answer doesn't exist in the context or chat history, say "I don't know."
    If the answer is related to chat history, give an appropriate answer.

    context: {context}
    """
    template = ChatPromptTemplate.from_messages([
        ("system", prompt),
        MessagesPlaceholder("history"),
        ("human", "{question}")
    ])
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)
    res = llm.invoke(template.format(question=query, history=chat_history, context=context))

    # Append both user and assistant message to chat_history
    new_chat_entries = [
        {
            "content": query,
            "sender": "Human",
            "timestamp": session_dict["timestamp"]
        },
        {
            "content": res.content,
            "sender": "Assistant",
            "timestamp": datetime.now(timezone.utc)
        }
    ]

    if existing_session:
        await db["chat_sessions"].update_one(
            {"_id": existing_session["_id"]},
            {
                "$push": {"messages": {"$each": new_chat_entries}},
                "$set": {"updatedAt": now}
            }
        )
        updated_session = await db["chat_sessions"].find_one({"_id": existing_session["_id"]})
    else:
        session_data = {
            "createdAt": now,
            "updatedAt": now,
            "user_id": user.id,
            "messages": new_chat_entries
        }
        result = await db["chat_sessions"].insert_one(session_data)
        updated_session = await db["chat_sessions"].find_one({"_id": result.inserted_id})

    return {
        "id": str(updated_session["_id"]),
        "user_id": updated_session["user_id"],
        "messages": updated_session["messages"],
        "createdAt": updated_session["createdAt"]
    }
