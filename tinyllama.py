import sys
from pathlib import Path
EXMAPLES_PATH = Path(__file__).resolve().parent.parent / "tinygrad/examples"
sys.path.append(EXMAPLES_PATH)

from examples.llama import LLaMa
from llama_cpp import Llama


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

class TinyLLaMA(LLaMa):
  def __init__(self):
    llama = self.build(MODEL_PATH, TOKENIZER_PATH, model_gen=gen, model_size=size, quantize=quantize)
    self.model = llama.model
    self.tokenizer = llama.tokenizer

if __name__ == "__main__":
  tiny = TinyLLaMA()
  print(tiny.model)
    