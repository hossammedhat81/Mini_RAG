from fastapi import FastAPI
app = FastAPI()

@app.get("/welcome")        #decorator required to tell FastAPI that the function immediately below is in charge of handling requests that go to the path "/welcome" using the GET HTTP method.
def welcome():
    return {
        "message":"Hello, welcome to the Mini RAG application!"
    }

