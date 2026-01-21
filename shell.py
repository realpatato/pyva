import pyva

while True:
    text = input("PYVA > ")
    if text == "end":
        break
    result, error = pyva.run("<Sys.in>", text)
    if error:
        print(error.as_string())
    else:
        print(result)