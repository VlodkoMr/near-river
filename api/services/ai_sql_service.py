import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
from fastapi import HTTPException

from config.settings import conf


class AISqlService:
    def __init__(self):
        if torch.cuda.is_available():
            self.model, self.tokenizer = self.setup_model()
        else:
            print("GPU is not available. AI requires GPU to process the request.")

    def setup_model(self):
        """
        Initialize model and tokenizer for AI usage (if available).
        """
        if not os.path.isdir(conf.AI_MODEL_ID) or not os.listdir(conf.AI_MODEL_ID):
            raise HTTPException(status_code=500, detail=f"Model directory '{conf.AI_MODEL_ID}' does not exist or is empty.")

        bnb_config = BitsAndBytesConfig(
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        tokenizer = AutoTokenizer.from_pretrained(conf.AI_MODEL_ID)
        model = AutoModelForCausalLM.from_pretrained(
            conf.AI_MODEL_ID,
            quantization_config=bnb_config,
            device_map="auto",
        )
        tokenizer.pad_token = tokenizer.eos_token
        return model, tokenizer

    def run_sql_command(self, question: str):
        if not torch.cuda.is_available():
            raise Exception("GPU is not available. AI requires GPU to process the request.")

        prompt = self.generate_sql_prompt(
            question,
            "config/prompts/sql_prompt.md",
            "/schema.postgresql.sql"
        )
        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=conf.AI_MODEL_MAX_TOKENS,
            do_sample=False,
            return_full_text=False,
            num_beams=conf.AI_MODEL_NUM_BEAMS,
        )

        # Generate SQL query based on the prompt
        generated_text = pipe(prompt, num_return_sequences=1)[0]["generated_text"]
        sql_query = self.extract_sql_query(generated_text)

        # Additional level of data protection - clean up the generated SQL query
        return self.clean_generated_sql(sql_query)

    def extract_sql_query(self, generated_text: str):
        """
        Extracts the SQL query from the generated text using a regular expression.
        """
        # Regex pattern to capture the SQL query
        sql_pattern = r"(?i)(SELECT\s+.*?;)"

        # Search for the SQL query in the generated text
        match = re.search(sql_pattern, generated_text, re.DOTALL)

        if match:
            # Return the captured SQL query
            return match.group(1).strip()
        else:
            raise ValueError("No valid SQL query found in the generated text")

    def clean_generated_sql(self, sql_query: str):
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
            raise HTTPException(status_code=400, detail="The query contains disallowed operations (only SELECT is permitted).")

        return sql_query

    def generate_sql_prompt(self, question: str, prompt_file: str, metadata_file: str):
        with open(prompt_file, "r") as prompt_f, open(metadata_file, "r") as meta_f:
            prompt = prompt_f.read().format(user_question=question, table_metadata_string=meta_f.read())
        return prompt

    # -------------------------------------------------------

    def generate_summary_prompt(self, question: str, data: dict, prompt_file: str):
        with open(prompt_file, "r") as prompt_f:
            prompt = prompt_f.read().format(user_question=question, data=data)
            return [
                {"role": "system", "content": prompt},
                {"role": "user", "content": question},
            ]

    def run_data_question_command(self, question: str, data: dict):
        if not torch.cuda.is_available():
            raise Exception("GPU is not available. AI requires GPU to process the request.")

        print('---------- question, data: ', question, data)

        prompt_messages = self.generate_summary_prompt(
            question,
            data,
            "config/prompts/summary_prompt.md",
        )

        print('---------- prompt_messages ', prompt_messages)

        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto",
            return_full_text=False,
        )

        outputs = pipe(
            prompt_messages,
            max_new_tokens=conf.AI_MODEL_MAX_TOKENS,
        )

        print('---------- outputs', outputs)

        return outputs[0]["generated_text"]