from io import BytesIO, StringIO
from uuid import UUID

import yaml
from fastapi import FastAPI, File, HTTPException
from fastapi.responses import PlainTextResponse

from app.BodyTypes import TypeStorageAnswer, ServiceTemplateDefinition
from mariadb_parser.ORM_model.GetData import TypeStorageGetter, InstanceModelGetter
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
async def get_type_storage_file(uuid: str) -> ServiceTemplateDefinition:
    try:
        data_getter = TypeStorageGetter(uuid)
        data_getter.get_types()
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")
    return data_getter.result


@app.get("/type-storage/{tosca_definitions_version}/{template_author}/{template_name}/{template_version}/raw",
         response_class=PlainTextResponse)
@app.head("/type-storage/{tosca_definitions_version}/{template_author}/{template_name}/{template_version}/raw",
          response_class=PlainTextResponse)
async def get_type_storage_file(tosca_definitions_version: str,
                                template_name: str,
                                template_version: str,
                                template_author: str):
    try:
        data_getter = TypeStorageGetter(tosca_definitions_version=tosca_definitions_version,
                                        template_name=template_name,
                                        template_version=template_version,
                                        template_author=template_author)
        data_getter.get_types()
        # answer.user = user_name
        # answer.file_name = file_name
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")
    return str(yaml.dump(data_getter.result)).encode("utf-8")


@app.post("/type-storage")
async def post_type_storage_file(tosca_types: ServiceTemplateDefinition) -> UUID:
    print(tosca_types.dict(), "\n", type(tosca_types))
    parsed_template = TypeStorage(tosca_types.dict(exclude_none=True))
    loader = DataUploader()
    loader.insert_type_storage(parsed_template)
    return UUID(parsed_template.database_id)


@app.post("/instance-model-storage/")
async def post_type_storage_file(service_template_definition: ServiceTemplateDefinition) -> UUID:
    service_template_definition: dict = service_template_definition.dict(exclude_none=True)
    # todo спрятать в класс
    if service_template_definition.get('imports'):
        for import_tosca in service_template_definition.get('imports'):
            imported_tosca = TypeStorageGetter(import_tosca)
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
