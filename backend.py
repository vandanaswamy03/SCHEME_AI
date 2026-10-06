
import chromadb
from sentence_transformers import SentenceTransformer
import ollama


# -----------------------------------
# LOAD EMBEDDING MODEL
# -----------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------------
# CHROMADB
# -----------------------------------

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="government_schemes"
)


# -----------------------------------
# LOAD SCHEMES
# -----------------------------------

def load_schemes():

    with open(
        "schemes.txt",
        "r",
        encoding="utf-8"
    ) as file:

        data = file.read()

    schemes = [
        scheme.strip()
        for scheme in data.split("\n\n")
        if scheme.strip()
    ]

    return schemes


# -----------------------------------
# ADD SCHEMES TO DATABASE
# -----------------------------------

def initialize_database():

    schemes = load_schemes()

    if collection.count() == 0:

        embeddings = model.encode(
            schemes
        ).tolist()

        collection.add(
            ids=[
                f"scheme_{i}"
                for i in range(len(schemes))
            ],
            documents=schemes,
            embeddings=embeddings
        )


# -----------------------------------
# SEARCH GOVERNMENT SCHEMES
# -----------------------------------

def search_schemes(
    user_query,
    number_of_results=3
):

    query_embedding = model.encode(
        [user_query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=number_of_results
    )

    return results["documents"][0]


# -----------------------------------
# GENERATE AI RESPONSE
# -----------------------------------

def generate_answer(
    user_query,
    scheme_results
):

    context = "\n\n".join(
        scheme_results
    )

    prompt = f"""
You are SCHEME AI, a Telangana Government Scheme Assistant.

IMPORTANT:
- This system is ONLY for people living in Telangana.
- Recommend ONLY Telangana-specific schemes.
- Do not recommend schemes from other states.
- Use ONLY the information provided in the context.
- Do not invent eligibility rules, benefits or documents.

User information:
{user_query}

Available Telangana scheme information:
{context}

Give a simple and clear answer.

Mention:
1. Suitable Telangana scheme
2. Eligibility
3. Benefits
4. Required documents
5. Application guidance

If suitable information is not available,
tell the user to verify the latest information
from the official Telangana government department.
"""

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception:

        return (
            "Ollama is not running or the selected "
            "model is not available. "
            "Please start Ollama and make sure the "
            "required model is installed."
        )


# -----------------------------------
# MAIN RAG FUNCTION
# -----------------------------------

def get_scheme_recommendation(
    user_query
):

    initialize_database()

    schemes = search_schemes(
        user_query
    )

    answer = generate_answer(
        user_query,
        schemes
    )

    return answer, schemes
