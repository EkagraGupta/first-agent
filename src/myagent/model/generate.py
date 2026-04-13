from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from dotenv import load_dotenv
import os

load_dotenv()
# TODO: Or add token globally using huggingface_hub's login() function call
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN not found")

class MyLLM:
    def __init__(
            self,
            model_id: str=None,
            use_4bit: bool=True,
            device: str="cuda",
    ):
        self.model_id = model_id
        self.use_4bit = use_4bit
        self.device = device

        self.tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)

        quantization_config = None
        if use_4bit:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map=device,
            torch_dtype="auto",
            quantization_config=quantization_config,
            token=HF_TOKEN,
        )

    @torch.inference_mode()
    def generate(self, prompt: str, max_new_tokens: int=50):
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.device)

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
        )

        new_tokens = output_ids[0][inputs.input_ids.shape[1]:] 
        text = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        return text.strip()
    
    