import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
from fastapi import HTTPException

from config.settings import conf


class AISummaryService:
    def __init__(self):
        self.model, self.tokenizer = self.setup_model()

    def setup_model(self):
        """
        Initialize model and tokenizer for AI usage (if available).
        """
        if torch.cuda.is_available():
            if not os.path.isdir(conf.AI_SUMMARY_MODEL_ID) or not os.listdir(conf.AI_SUMMARY_MODEL_ID):
                raise HTTPException(status_code=500, detail=f"Model directory '{conf.AI_SUMMARY_MODEL_ID}' does not exist or is empty.")

            bnb_config = BitsAndBytesConfig(
                load_in_4bits=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            tokenizer = AutoTokenizer.from_pretrained(conf.AI_SUMMARY_MODEL_ID)
            model = AutoModelForCausalLM.from_pretrained(
                conf.AI_SUMMARY_MODEL_ID,
                quantization_config=bnb_config,
                device_map="auto",
            )
            tokenizer.pad_token = tokenizer.eos_token
            return model, tokenizer
        else:
            raise HTTPException(status_code=503, detail="GPU is not available. AI requires GPU to process the request.")

    def run_question_command(self, question: str, data: dict):
        prompt_messages = self.generate_summary_prompt(
            question,
            data,
            "config/prompts/summary_prompt.md",
        )

        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto",
            return_full_text=False,
        )

        outputs = pipe(
            prompt_messages,
            max_new_tokens=conf.AI_SUMMARY_MODEL_MAX_TOKENS,
        )

        print('outputs', outputs)

        return outputs[0]["generated_text"][-1]

    def generate_summary_prompt(self, question: str, data: dict, prompt_file: str):
        # with open(prompt_file, "r") as prompt_f:
        #     prompt = prompt_f.read().format(user_question=question, data=data)
        # return prompt
        return [
            {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
            {"role": "user", "content": "Who are you?"},
        ]
