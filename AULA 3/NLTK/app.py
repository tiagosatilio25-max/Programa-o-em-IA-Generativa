import nltk


# 1. Garante que os recursos necessários estão descarregados
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger_eng")

frase = "Livia, isso é uma frase"

# 2. Tokeniza a frase corretamente
tokens = nltk.word_tokenize(frase, language="portuguese")
sig = nltk.pos_tag(tokens)

# 3. Imprime a frase e os tokens gerados
print("Frase original:", frase)
print("Tokens:", tokens)
print(sig)