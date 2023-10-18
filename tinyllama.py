import sys
from pathlib import Path
import importlib

from personality import load_personality
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
  def __init__(self, personality='george'):
    self.llama = LLaMa.build(MODEL_PATH, TOKENIZER_PATH, model_gen=gen, model_size=size, quantize=quantize)
    self.personality = load_personality(personality)

  @property
  def eot_token_id(self):
    # we use EOT because end of *text* is more accurate for what we're doing than end of *sentence*
    return self.llama.tokenizer.eos_id()

  @property
  def bos_token_id(self): return self.llama.tokenizer.bos_id()
  @property
  def max_length(self): return 1024
  @property
  def max_gen_toks(self): return 256
  @property
  def batch_size(self): return 1
    





  def prepare(self, personality: str):
    self.toks = [self.llama.tokenizer.bos_id()] + self.encode(self.personalities[personality])

  def create_chat_completion(self, msg: str):
    ...

  def tok_encode(self, prompt: str):
    return self.llama.tokenizer.encode(prompt)
  def tok_decode(self, tokens):
    return self.llama.tokenizer.decode(prompt)
  

if __name__ == "__main__":
  tiny = TinyLLaMA()
  tiny.prepare("geohot")
  tiny.create_chat_completion()
    