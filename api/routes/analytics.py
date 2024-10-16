import torch
import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from helpers.decorators import exception_handler

router = APIRouter()

# Check if GPU is available
model = None
tokenizer = None
gpu_enabled = torch.cuda.is_available()

if gpu_enabled:
    # Prepare model and tokenizer for faster response
    model_id = "config/ai_models/sqlcoder-7b-2"
    bnb_config = BitsAndBytesConfig(
        load_in_4bits=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
    )


class QuestionRequest(BaseModel):
    question: str = ""


@router.post("/ask")
@exception_handler
async def get_analytics_question(request: QuestionRequest):
    if not gpu_enabled:
        raise HTTPException(status_code=503, detail="GPU is not available. AI requires GPU to process the request.")

    if request.question == "":
        raise HTTPException(status_code=400, detail="Question is required to process the request.")

    question = request.question
    print(f"Received question: {question}")

    _default_question = "Select latest publications on near social"
    parser = argparse.ArgumentParser(description="Run inference on a question")
    parser.add_argument("-q", "--question", type=str, default=_default_question, help="Question to run inference on")
    result = run_inference(question)

    return {"question": question, "answer": result}


def run_inference(question):
    prompt_file = "config/ai_data/prompt.md"
    metadata_file = "/schema.postgresql.sql"
    prompt = generate_prompt(question, prompt_file, metadata_file)

    # make sure the model stops generating at triple ticks
    # eos_token_id = tokenizer.convert_tokens_to_ids(["```"])[0]
    # eos_token_id = tokenizer.eos_token_id

    pipe_call = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        do_sample=False,
        return_full_text=False,
        num_beams=1,
    )

    generated_query = (
        pipe_call(
            prompt,
            num_return_sequences=1
        )[0]["generated_text"]
    )
    return generated_query


def generate_prompt(question, prompt_file, metadata_file):
    with open(prompt_file, "r") as f:
        prompt = f.read()

    with open(metadata_file, "r") as f:
        table_metadata_string = f.read()

    prompt = prompt.format(
        user_question=question, table_metadata_string=table_metadata_string
    )
    print(prompt)
    return prompt
