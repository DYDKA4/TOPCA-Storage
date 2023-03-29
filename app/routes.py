from uuid import UUID

import yaml
from fastapi import FastAPI, File, HTTPException

from app.BodyTypes import TypeStorageAnswer, ServiceTemplateDefinition
from mariadb_parser.ORM_model.DataGetter import DataGetter, InstanceModelGetter
from mariadb_parser.ORM_model.InsertData import DataUploader, InstanceModelUploader
from mariadb_parser.instance_model.NormalizedTOSCA import InstanceModel
from mariadb_parser.instance_model.instance_model import InstanceModelInternal
from mariadb_parser.instance_model.parse_puccini import TopologyTemplateInstance
from mariadb_parser.instance_model.puccini_try import puccini_parse
from mariadb_parser.type_table.TypeStorage import TypeStorage
from pydantic.utils import deep_update
from app.base_types import base_types
import collections
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/type-storage/{uuid}")
async def get_type_storage_file(uuid: str) -> TypeStorageAnswer:
    try:
        data_getter = DataGetter(uuid)
        data_getter.get_types()
        answer = TypeStorageAnswer()
        # answer.user = user_name
        # answer.file_name = file_name
        answer.result = data_getter.result
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")
    return answer


@app.post("/type-storage/")
async def post_type_storage_file(tosca_types: ServiceTemplateDefinition) -> None:
    # print(tosca_types.dict(), "\n", type(tosca_types))
    parsed_template = TypeStorage(tosca_types.dict(exclude_none=True))
    loader = DataUploader()
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
    parsed_template = TypeStorage(tosca_types.dict(exclude_none=True))
    loader = DataUploader('tosca_simple_yaml_1_3', f'{user_name}/{dir_name}/{file_name}')
    loader.insert_type_storage(parsed_template)
    return None


@app.post("/instance-model-storage/")
async def post_type_storage_file(service_template_definition: ServiceTemplateDefinition) -> UUID:
    service_template_definition: dict = service_template_definition.dict(exclude_none=True)
    #todo спрятать в класс
    if service_template_definition.get('imports'):
        for import_tosca in service_template_definition.get('imports'):
            imported_tosca = DataGetter(import_tosca)
            imported_tosca.get_types()
            service_template_definition = deep_update(service_template_definition, imported_tosca.result)
        service_template_definition.pop("imports")
    service_template_definition = deep_update(service_template_definition, base_types)
    with open("output.yaml", "w") as f:
        f.write(yaml.dump(service_template_definition))
    template: str = yaml.dump(service_template_definition)
    topology = puccini_parse(template.encode("utf-8"))
    topology = TopologyTemplateInstance("None", topology)
    data = InstanceModelInternal(topology.render())
    uploader = InstanceModelUploader(data)
    uploader.insert_instance_model()
    return UUID(data.database_id)


@app.post("/instance-model-storage/normalized-tosca")
async def post_type_storage_file(tosca_types: InstanceModel) -> UUID:
    data = InstanceModelInternal(tosca_types.dict())
    uploader = InstanceModelUploader(data)
    uploader.insert_instance_model()
    return UUID(data.database_id)

@app.get("/instance-model-storage/{uuid}")
async def post_type_storage_file(uuid: str) -> InstanceModel:
    instance_model = InstanceModelGetter(uuid)
    instance_model.construct_instance_model()
    print(instance_model.instance_model)
    with open("output.yaml", 'w') as stream:
        stream.write(yaml.dump(instance_model.instance_model.dict()))
    return instance_model.instance_model
