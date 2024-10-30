import torch
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.database_service import DatabaseService
from helpers.decorators import exception_handler
from services.ai_model_service import AIModelService

router = APIRouter()

ai_model_service = AIModelService()


class SQLGenerateRequest(BaseModel):
    question: str = ""


@router.post("/sql-generate")
@exception_handler
async def get_analytics_sql(request: SQLGenerateRequest):
    result_sql = ''
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question is required to process the request.")

    try:
        # Use the AI service to generate SQL query based on the question
        result_sql = ai_model_service.run_sql_command(question)
        print('Result SQL: ', result_sql)
    except Exception as e:
        return {
            "question": question,
            "sql": result_sql,
            "error": str(e)
        }

    return {
        "question": question,
        "sql": result_sql,
    }


class SQLDataRequest(BaseModel):
    sql: str = ""


@router.post("/sql-data")
@exception_handler
async def get_analytics_sql_results(request: SQLDataRequest):
    sql = request.sql.strip()

    if not sql:
        raise HTTPException(status_code=400, detail="SQL is required to process the request.")

    try:
        # Check and clean the SQL query
        result_sql = ai_model_service.clean_generated_sql(sql)

        # Try to execute generated SQL query and return the result
        async with DatabaseService() as db:
            query_data = await db.run_raw_sql(result_sql)
    except Exception as e:
        return {
            "sql": sql,
            "error": str(e)
        }

    return {
        "sql": result_sql,
        "data": query_data
    }


class SummaryQuestionRequest(BaseModel):
    sql_question: str = ""
    data_question: str = ""


@router.post("/question")
@exception_handler
async def get_analytics_question(request: SummaryQuestionRequest):
    sql_question = request.sql_question.strip()
    data_question = request.data_question.strip()
    result_sql = ''

    if not sql_question or not data_question:
        raise HTTPException(status_code=400, detail="Question is required to process the request.")

    try:
        # Use the AI service to generate SQL query based on the question
        result_sql = ai_model_service.run_sql_command(sql_question)
        print('Result SQL: ', result_sql)

        torch.cuda.empty_cache()

        # Try to execute generated SQL query and return the result
        async with DatabaseService() as db:
            query_data = await db.run_raw_sql(result_sql)
            print('Query Data: ', query_data)

            # Use the AI service to generate summary based on the question and data
            result_answer = ai_model_service.run_data_question_command(sql_question, data_question, query_data)

    except Exception as e:
        return {
            "sql_question": sql_question,
            "data_question": data_question,
            "sql": result_sql,
            "error": str(e)
        }

    return {
        "sql_question": sql_question,
        "data_question": data_question,
        "answer": result_answer,
        "sql": result_sql,
        "data": query_data,
    }
