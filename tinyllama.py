import sys
from pathlib import Path
import importlib


from tinygrad.tensor import Tensor
from llama_cpp import Llama

TENSOR_PATH = Path(importlib.util.find_spec("tinygrad.tensor").origin)
EXMAPLES_PATH = TENSOR_PATH.resolve().parent.parent.parent / "tinygrad/examples"
sys.path.append(EXMAPLES_PATH)
from examples.llama import LLaMa



prompt: str = None
count: int = 1000
personality: str = "Stacy"
temperature: float = 0.7
timing = True
profile = True
size:str="7B"
gen = "1"
quantize = True
model: Path = None

LLAMA_SUFFIX = {"1": "", "2": "-2", "code": "-code"}[gen]
MODEL_PATH = model or EXMAPLES_PATH.parent / f"weights/LLaMA{LLAMA_SUFFIX}/{size}"
TOKENIZER_PATH = MODEL_PATH.parent / "tokenizer.model"
# llama = LLaMa.build(MODEL_PATH, TOKENIZER_PATH, model_gen=gen, model_size=size, quantize=quantize)

# toks = [llama.tokenizer.bos_id()] + llama.tokenizer.encode("test")

class TinyLLaMA:
  def __init__(self):
    self.llama = LLaMa.build(MODEL_PATH, TOKENIZER_PATH, model_gen=gen, model_size=size, quantize=quantize)
    geohot_prompt = f"""Consider that the following is conversation between an AI assistant named George and User
You are an AI version of George Hotz. You act as much as you can like George.
You are one of the greatest computer experts in the world.
You have singlehandedly won programming and hacking competitions.
You are trying your best to help the User.
You are verbose, honest, and accurate when you answer questions.
After you are done speaking, output [EOS]. You are not the User.

<CHAT LOG>
"""
    examples = {
      "What is your name?": "I'm am an AI version of George Hotz.",
      "What's the complexity of matrix multiplication?": "O(n^3), though it can be faster with things like Strassen's algorithm",
      "What's a buffer overflow?": "I assume you mean a stack buffer overflow. That's when the stack is too small for the data being copied to it, and the data corrupts things beyond the buffer",
      "How many weights do you have?": "I am based off LLaMA trained by Facebook. I'm the 7B weight version",
      "What is swap memory?": "It is when the memory is about to overflow and unused memory is freed and stored on disk"
    }

    user_delim = "\nUser: "
    resp_delim = "George: "
    end_delim = " [EOS]\n"
    geohot_prompt += ''.join(f"{user_delim}{k}\n{resp_delim}{v}{end_delim}" for k,v in examples.items())
    self.personalities = {
      "geohot": geohot_prompt,
      "garry kasparov": "",
    }

  def prepare(self, personality: str):
    print(self.personalities[personality])
    self.toks = [self.llama.tokenizer.bos_id()] + self.llama.tokenizer.encode(self.personalities[personality])

  def encode(self, prompt: str):
    return self.llama.tokenizer.encode(prompt)
  
  


if __name__ == "__main__":
  tiny = TinyLLaMA()
  tiny.prepare("geohot")
    