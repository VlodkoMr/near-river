import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
from fastapi import HTTPException

from config.settings import conf


class AISqlService:
    def __init__(self):
        self.model, self.tokenizer = self.setup_model()

    def setup_model(self):
        """
        Initialize model and tokenizer for AI usage (if available).
        """
        if torch.cuda.is_available():
            if not os.path.isdir(conf.AI_SQL_MODEL_ID) or not os.listdir(conf.AI_SQL_MODEL_ID):
                raise HTTPException(status_code=500, detail=f"Model directory '{conf.AI_SQL_MODEL_ID}' does not exist or is empty.")

            bnb_config = BitsAndBytesConfig(
                load_in_4bits=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            tokenizer = AutoTokenizer.from_pretrained(conf.AI_SQL_MODEL_ID)
            model = AutoModelForCausalLM.from_pretrained(
                conf.AI_SQL_MODEL_ID,
                quantization_config=bnb_config,
                device_map="auto",
            )
            tokenizer.pad_token = tokenizer.eos_token
            return model, tokenizer
        else:
            raise HTTPException(status_code=503, detail="GPU is not available. AI requires GPU to process the request.")

    def run_sql_command(self, question: str):
        prompt = self.generate_sql_prompt(
            question,
            "config/prompts/sql_prompt.md",
            "/schema.postgresql.sql"
        )
        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=conf.AI_SQL_MODEL_MAX_TOKENS,
            do_sample=False,
            return_full_text=False,
            num_beams=conf.AI_SQL_MODEL_NUM_BEAMS,
        )

        # Generate SQL query based on the prompt
        generated_text = pipe(prompt, num_return_sequences=1)[0]["generated_text"]

        # Additional level of data protection - clean up the generated SQL query
        return self.clean_generated_sql(generated_text)

    def clean_generated_sql(self, generated_text: str):
        """
            Cleans the generated SQL query to ensure it's read-only. Only allows queries that start
            with a SELECT statement and disallows any potentially harmful operations.
            """
        # Extract only from the first SELECT statement to ensure it's a read-only query
        sql_start = generated_text.upper().find("SELECT")
        if sql_start == -1:
            raise HTTPException(status_code=400, detail="Only SELECT queries are allowed.")

        sql_query = generated_text[sql_start:].strip()

        # Reject queries that contain anything after SELECT that could modify data
        disallowed_keywords = [
            r"\bINSERT \b",  # Insert data
            r"\bUPDATE \b",  # Update data
            r"\bDELETE \b",  # Delete data
            r"\bDROP \b",  # Drop tables or databases
            r"\bALTER \b",  # Alter tables
            r"\bCREATE\b",  # Create tables/databases
            r"\bTRUNCATE\b",  # Truncate tables
            r"\bREPLACE\b",  # Replace data
            r"\bMERGE\b",  # Merge operations
            r"\bEXECUTE\b",  # Execute procedures or functions
            r"\bCALL\b",  # Call stored procedures
            r"\bGRANT\b",  # Grant permissions
            r"\bREVOKE\b",  # Revoke permissions
            r"\bLOCK\b",  # Lock tables
            r"\bUNLOCK\b"  # Unlock tables
        ]

        # If any disallowed keyword exists, reject the query
        if any(re.search(keyword, sql_query, re.IGNORECASE) for keyword in disallowed_keywords):
            raise HTTPException(status_code=400, detail="The query contains disallowed operations (only SELECT is permitted).")

        return sql_query

    def generate_sql_prompt(self, question: str, prompt_file: str, metadata_file: str):
        with open(prompt_file, "r") as prompt_f, open(metadata_file, "r") as meta_f:
            prompt = prompt_f.read().format(user_question=question, table_metadata_string=meta_f.read())
        return prompt
