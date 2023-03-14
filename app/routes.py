import yaml
from fastapi import FastAPI, File, HTTPException

from app.BodyTypes import TypeStorageAnswer, ServiceTemplateDefinition
from mariadb_parser.ORM_model.DataGetter import DataGetter
from mariadb_parser.ORM_model.InsertData import DataUploader
from mariadb_parser.instance_model.parse_puccini import TopologyTemplateInstance
from mariadb_parser.instance_model.puccini_try import puccini_parse
from mariadb_parser.type_table.TypeStorage import TypeStorage

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
        raise HTTPException(status_code=500, detail="internal error")
    return answer


@app.post("/type-storage/{user_name}/{file_name}")
async def post_type_storage_file(user_name: str, file_name: str, tosca_types: ServiceTemplateDefinition) -> None:
    # print(tosca_types.dict(), "\n", type(tosca_types))
    parsed_template = TypeStorage(tosca_types.dict())
    loader = DataUploader('tosca_simple_yaml_1_3', f'{user_name}/{file_name}')
    loader.insert_type_storage(parsed_template)
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


@app.post("/type-storage/{user_name}/{dir_name}/{file_name}")
async def post_type_storage_file(user_name: str, dir_name: str, file_name: str,
                                 tosca_types: ServiceTemplateDefinition) -> None:
    # print(tosca_types.dict(), "\n", type(tosca_types))
    parsed_template = TypeStorage(tosca_types.dict())
    loader = DataUploader('tosca_simple_yaml_1_3', f'{user_name}/{dir_name}/{file_name}')
    loader.insert_type_storage(parsed_template)
    return None


@app.post("/instance-model-storage")
async def post_type_storage_file(tosca_types: ServiceTemplateDefinition) -> None:
    template: str = yaml.dump(tosca_types.dict(exclude_none=True))
    with open("template.yaml", "w") as file:
        file.write(template)
    topology = puccini_parse(template.encode("utf-8"))
    topology = TopologyTemplateInstance("None", topology)
    print(yaml.dump(topology.render()))
    return
