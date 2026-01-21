import pyva

while True:
    text = input("PYVA > ")
    result, error = pyva.run("<Sys.in>", text)
    if error:
        print(error.as_string())
    else:
        print(result)