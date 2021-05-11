from ckiptagger import WS

poem = "牀前看月光，疑是地上霜。舉頭望山月，低頭思故鄉。"
ws = WS("./data/data")
results = ws([poem])[0]
print(results)