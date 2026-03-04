import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings 
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# configuration constants
EMBEDDING_MODEL_NAME = 'text-embedding-3-large'
persist_directory = './chroma_db'
MODEL_DEPLOYMENT_NAME = "gpt-4.1"  # 실제 Azure 배포명을 입력하세요

# create embedding model and vector store
embedding_model = AzureOpenAIEmbeddings(
    azure_deployment=EMBEDDING_MODEL_NAME, 
    chunk_size=1000
)

db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_model
)

from langchain_classic.chains import RetrievalQA 
from langchain_openai import AzureChatOpenAI

# language model for retrieval QA
llm = AzureChatOpenAI(
    deployment_name=MODEL_DEPLOYMENT_NAME,
    temperature=1,
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=db.as_retriever(
        search_type='mmr',
        search_kwargs={'k': 3, 'fetch_k': 10}
    ),
    return_source_documents=True
)

# --- Streamlit app --------------------------------------------------------

def chat_interface():
    st.title("📚 벡터 검색 기반 챗봇")
    st.write("Azure OpenAI와 Chroma 벡터스토어를 활용한 질의응답 시스템입니다.")

    # initialize history
    if 'history' not in st.session_state:
        st.session_state.history = []  # list of (user, assistant, sources)

    # user input
    with st.form(key='query_form', clear_on_submit=True):
        query = st.text_input("질문을 입력하세요", key='input')
        submit = st.form_submit_button("전송")

    if submit and query:
        with st.spinner("답변을 검색하는 중..."):
            result = qa.invoke(query)
            answer = result['result']
            sources = result.get('source_documents', [])

        # append to history
        st.session_state.history.append((query, answer, sources))

    # display conversation
    for user_q, ans, src_docs in st.session_state.history:
        st.markdown(f"**사용자:** {user_q}")
        st.markdown(f"**응답:** {ans}")
        if src_docs:
            with st.expander("소스 문서 보기"):
                for doc in src_docs:
                    st.markdown(f"- {doc.metadata.get('source', 'unknown')} : {doc.page_content[:200]}...")
        st.markdown("---")


if __name__ == '__main__':
    chat_interface()



