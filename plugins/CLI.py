import typer
app = typer.Typer()

@app.command()
def echo(get: str=typer.Argument(...)):
    print(get)
@app.command()
def qwq():
    print("qwq")
if __name__ == "__main__":
    app()
