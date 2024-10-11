import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import argparse

from fastapi import APIRouter
from pydantic import BaseModel
from helpers.decorators import exception_handler

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str = "How much transactions we have?"


@router.post("/ask")
@exception_handler
async def get_analytics_question(request: QuestionRequest):
    question = request.question
    print(f"Received question: {question}")

    _default_question = "How much transactions we have?"
    parser = argparse.ArgumentParser(description="Run inference on a question")
    parser.add_argument("-q", "--question", type=str, default=_default_question, help="Question to run inference on")
    result = run_inference(question)
    print('RESULTS: ', result)

    return {"question": question, "answer": result}


def run_inference(question):
    tokenizer, model = get_tokenizer_model("config/ai_models/sqlcoder-7b-2")
    prompt_file = "config/ai_data/prompt.md"
    metadata_file = "/schema.postgresql.sql"
    prompt = generate_prompt(question, prompt_file, metadata_file)

    print('>>>>>>>>>>>>>>>> prompt ', prompt)

    # make sure the model stops generating at triple ticks
    # eos_token_id = tokenizer.convert_tokens_to_ids(["```"])[0]
    eos_token_id = tokenizer.eos_token_id

    print('>>>>>>>>>>>>>>>> eos_token_id ', eos_token_id)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=300,
        do_sample=False,
        return_full_text=False,  # added return_full_text parameter to prevent splitting issues with prompt
        num_beams=4,  # do beam search with 5 beams for high quality results
    )

    print('>>>>>>>>>>>>>>>> pipe: ', pipe)

    generated_query = (
            pipe(
                prompt,
                num_return_sequences=1,
                eos_token_id=eos_token_id,
                pad_token_id=eos_token_id,
            )[0]["generated_text"]
            .split(";")[0]
            .split("```")[0]
            .strip()
            + ";"
    )
    print('>>>>>>>>>> generated_query', generated_query)
    return generated_query


def get_tokenizer_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map="auto",
        use_cache=True,
    )
    return tokenizer, model


def generate_prompt(question, prompt_file, metadata_file):
    with open(prompt_file, "r") as f:
        prompt = f.read()

    with open(metadata_file, "r") as f:
        table_metadata_string = f.read()

    prompt = prompt.format(
        user_question=question, table_metadata_string=table_metadata_string
    )
    return prompt
