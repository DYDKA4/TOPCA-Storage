from fastapi import FastAPI, File, HTTPException

from app.BodyTypes import TypeStorageAnswer, ServiceTemplateDefinition
from mariadb_parser.ORM_model.InsertData import DataGetter

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/type-storage/{user_name}/{file_name}")
async def get_type_storage_file(user_name: str, file_name: str) -> TypeStorageAnswer:
    try:
        data_getter = DataGetter(user_name + "/" + file_name)
        data_getter.get_types()
        answer = TypeStorageAnswer()
        answer.user = user_name
        answer.file_name = file_name
        answer.result = data_getter.result
    except Exception:
        raise HTTPException(status_code=500)
    return answer


@app.post("/type-storage/{user_name}/{file_name}")
async def post_type_storage_file(user_name: str, file_name: str, tosca_types: ServiceTemplateDefinition) -> None:
    return None


@app.get("/type-storage/{user_name}/{dir_name}/{file_name}")
async def get_type_storage_file(user_name: str, dir_name: str, file_name: str) -> TypeStorageAnswer:
    try:
        data_getter = DataGetter(user_name + "/" + dir_name + "/" + file_name)
        data_getter.get_types()
        answer = TypeStorageAnswer()
        answer.user = user_name
        answer.file_name = file_name
        answer.result = data_getter.result
    except Exception:
        raise HTTPException(status_code=500)
    return answer
