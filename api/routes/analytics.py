import os
import torch
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
from services.database_service import DatabaseService
from tortoise.exceptions import OperationalError
from helpers.decorators import exception_handler

router = APIRouter()

def setup_model():
    """ Initialize model and tokenizer for AI usage (if available). """
    if torch.cuda.is_available():
        model_id = "config/ai_models/sqlcoder-7b-2"
        if not os.path.isdir(model_id) or not os.listdir(model_id):
            raise HTTPException(status_code=500, detail=f"Model directory '{model_id}' does not exist or is empty.")

        bnb_config = BitsAndBytesConfig(
            load_in_4bits=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map="auto",
        )
        tokenizer.pad_token = tokenizer.eos_token
        return model, tokenizer
    else:
        raise HTTPException(status_code=503, detail="GPU is not available. AI requires GPU to process the request.")

model, tokenizer = setup_model()

class QuestionRequest(BaseModel):
    question: str = ""

@router.post("/ask")
@exception_handler
async def get_analytics_question(request: QuestionRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required to process the request.")

    result_sql = run_inference(question)

    # Try to execute generated SQL query and return the result
    try:
        query_data = await execute_query(result_sql)
    except OperationalError as e:
        return {"question": question, "sql": result_sql, "error": str(e)}

    return {"question": question, "sql": result_sql, "data": query_data}

def run_inference(question: str):
    prompt = generate_prompt(question, "config/ai_data/prompt.md", "/schema.postgresql.sql")

    # Ensure the pipeline only returns the generated text (SQL query) and not the full prompt
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        do_sample=False,
        return_full_text=False
    )

    # Generate SQL query based on the prompt
    generated_text = pipe(prompt, num_return_sequences=1)[0]["generated_text"]

    # Clean up the generated SQL query (ensure it's not returning parts of the prompt or extra text)
    generated_sql = clean_generated_sql(generated_text)

    return generated_sql

def clean_generated_sql(generated_text: str):
    # Remove anything that might be a part of the prompt or non-SQL statements
    sql_start = generated_text.find("SELECT")
    if sql_start != -1:
        return generated_text[sql_start:].strip()
    return generated_text.strip()

def generate_prompt(question: str, prompt_file: str, metadata_file: str):
    with open(prompt_file, "r") as prompt_f, open(metadata_file, "r") as meta_f:
        prompt = prompt_f.read().format(user_question=question, table_metadata_string=meta_f.read())
    return prompt

async def execute_query(sql: str):
    async with DatabaseService() as db:
        return await db.run_raw_sql(sql)
