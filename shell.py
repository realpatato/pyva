import pyva

while True:
    text = input("PYVA > ")
    result, error = pyva.run(text)
    if error:
        print(error.as_string())
    else:
        print(result)