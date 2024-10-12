import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import argparse

from fastapi import APIRouter
from pydantic import BaseModel
from helpers.decorators import exception_handler

router = APIRouter()

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
    question: str = "Select latest 10 publications on near social"


@router.post("/ask")
@exception_handler
async def get_analytics_question(request: QuestionRequest):
    question = request.question
    print(f"Received question: {question}")

    _default_question = "Select latest publications on near social"
    parser = argparse.ArgumentParser(description="Run inference on a question")
    parser.add_argument("-q", "--question", type=str, default=_default_question, help="Question to run inference on")
    result = run_inference(question)

    print('RESULTS: ', result)

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
        max_new_tokens=128,
        do_sample=False,
        return_full_text=False,  # added return_full_text parameter to prevent splitting issues with prompt
        num_beams=1,  # do beam search with 5 beams for high quality results
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
    return prompt