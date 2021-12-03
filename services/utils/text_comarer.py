from nltk.tokenize import word_tokenize
import difflib as df
    
def str_comparer(txt1: str, txt2: str) -> float:
  t1_s = word_tokenize(txt1)
  t2_s = word_tokenize(txt2)
  return df.SequenceMatcher(None, t1_s, t2_s).ratio()
