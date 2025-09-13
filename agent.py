from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from dotenv import load_dotenv
import os

from schema import QuerySchema

load_dotenv()

db = SQLDatabase.from_uri("sqlite:///./database.sqlite")


# google api key from environment variable
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

llm_with_str_output = llm.with_structured_output(QuerySchema)


def generate_query(user_query: str, instruction: str, top_k: int = 5) -> str:

    table_info = db.get_table_info()
    dialect = db.dialect

    prompt = f"""
    You are an expert SQL query generator. Given the following database table information and SQL dialect,

    table_info: {table_info}

    dialect: {dialect}

    Instruction: {instruction}
    Generate an SQL query to answer the user's question.
    Make sure following things while generating the SQL query:
    1. Use the correct SQL dialect.
    2. Ensure the SQL query is syntactically correct.
    3. Use appropriate table and column names from the provided table information.
    4. Avoid using any columns or tables that do not exist in the provided table information.
    5. If it is read query, limit the results to top {top_k} rows.
    6. Handle complex aggregations and multi-table joins.

    user_query: {user_query}


    """

    response = llm_with_str_output.invoke(prompt)

    return response.query


def execute_query(query: str):
    result = db.run(query)
    return result


def get_response(user_query: str, instruction: str, sql_query: str):

    retry = 0

    try:
        query_result = execute_query(sql_query)
    except Exception as e:
        print(str(e))
        if retry < 3:
            retry += 1
            new_query = f"""
            The previous SQL query generated was: {sql_query}.
            It caused the following error when trying to process it: {str(e)}.
            Please regenerate the SQL query to fix the error.
            Make sure to follow the same guidelines as before.
            query: {user_query}
            """
            sql_query = generate_query(new_query, instruction, 5)
            query_result = get_response(user_query, instruction, sql_query)
        else:
            return "Error in generating SQL query."

    return query_result


def process_query(user_query: str, instruction: str) -> str:
    sql_query = generate_query(user_query, 5, instruction)
    print(f"Generated SQL Query: {sql_query}")

    query_response = get_response(
        user_query=user_query, instruction=instruction, sql_query=sql_query
    )

    prompt = f"""
    You are an expert data analyst. Given the following SQL query and its result, generate a concise and informative response to the user's query.
    Make sure the response is easy to understand and provides insights based on the data.
    SQL Query: {sql_query}
    SQL Query Result: {query_response}
    User Query: {user_query}
    Generate a concise and informative response to the user's query.
    """

    llm_response = llm.invoke(prompt)

    return llm_response.content
