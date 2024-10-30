import re
from fastapi import HTTPException


def generate_sql_prompt(question: str, prompt_file: str):
    with open(prompt_file, "r") as prompt_f:
        prompt = prompt_f.read().format(user_question=question)
    return prompt


def extract_sql_query(generated_text: str):
    """
    Extracts the SQL query from the generated text using a regular expression.
    """
    sql_pattern = r"(?i)(SELECT\s+.*?;)"
    match = re.search(sql_pattern, generated_text, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        raise ValueError("No valid SQL query found in the generated text")


def clean_generated_sql(sql_query: str):
    """
    Cleans the generated SQL query to ensure it's read-only. Only allows queries that start
    with a SELECT statement and disallows any potentially harmful operations.
    """
    sql_query = sql_query.replace("\n", " ")

    # Reject queries that contain anything other than SELECT
    disallowed_keywords = [
        r"\bINSERT\b", r"\bUPDATE\b", r"\bDELETE\b", r"\bDROP\b",
        r"\bALTER\b", r"\bCREATE\b", r"\bTRUNCATE\b", r"\bREPLACE\b",
        r"\bMERGE\b", r"\bEXECUTE\b", r"\bCALL\b", r"\bGRANT\b",
        r"\bREVOKE\b", r"\bLOCK\b", r"\bUNLOCK\b"
    ]

    # If any disallowed keyword exists, reject the query
    if any(re.search(keyword, sql_query, re.IGNORECASE) for keyword in disallowed_keywords):
        raise HTTPException(
            status_code=400,
            detail="The query contains disallowed operations (only SELECT is permitted)."
        )

    return sql_query
