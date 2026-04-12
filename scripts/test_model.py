import time
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

def load_model(model_id: str, use_4bit: bool=False, device: str="cuda"):
    print(f"Loading tokenizer for {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    quantization_config = None
    if use_4bit:
        print("Using 4-bit quantization...")
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

    print(f"Loading model: {model_id}...")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map=device,
        torch_dtype="auto",
        quantization_config=quantization_config,
    )

    return tokenizer, model

@torch.inference_mode()
def run_chat_test(tokenizer, model, prompt: str):
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        [text],
        return_tensors="pt",
    ).to(model.device)

    print(f"Generating response...")
    start = time.time()
    output_ids = model.generate(
        **inputs,
        max_new_tokens=500,
        do_sample=False,
        temperature=None,
    )
    elapsed = time.time() - start

    new_tokens = output_ids[0][inputs.input_ids.shape[1]:]
    response = tokenizer.decode(new_tokens, skip_special_tokens=True)

    print(f"Response: {response}")
    print(f"Generation time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    model_id = "Qwen/Qwen3-4B-Instruct-2507"
    prompt = "What is the capital of France?"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    tokenizer, model = load_model(model_id, use_4bit=True, device=device)
    run_chat_test(tokenizer, model, prompt)