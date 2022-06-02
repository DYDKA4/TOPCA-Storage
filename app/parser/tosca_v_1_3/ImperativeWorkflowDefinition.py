# <workflow_name>:
#   description: <workflow_description>
#   metadata:
#     <map of string>
#   inputs:
#     <property_definitions>
#   preconditions:
#    - <workflow_precondition_definition>
#   steps:
#     <workflow_steps>
#   implementation:
#     <operation_implementation_definitions>
#   outputs:
#     <attribute_mappings>
from app.parser.tosca_v_1_3.DescriptionDefinition import description_parser
from app.parser.tosca_v_1_3.Metadata import Metadata
from app.parser.tosca_v_1_3.PropertyDefinition import PropertyDefinition, property_definition_parser
from app.parser.tosca_v_1_3.WorkflowPreconditionDefinition import WorkflowPredictionDefinition, \
    workflow_prediction_definition_parser


class ImperativeWorkflowDefinition:
    def __init__(self, name: str):
        self.vid = None
        self.vertex_type_system = 'ImperativeWorkflowDefinition'
        self.description = None
        self.name = name
        self.metadata = []
        self.inputs = []
        self.predictions = []
        self.steps = []

    def set_description(self, description: str):
        self.description = description

    def add_metadata(self, metadata: Metadata):
        self.metadata.append(metadata)

    def add_inputs(self, inputs: PropertyDefinition):
        self.inputs.append(inputs)

    def add_prediction(self, prediction: WorkflowPredictionDefinition):
        self.predictions.append(prediction)


def imperative_workflow_parser(name: str, data: dict) -> ImperativeWorkflowDefinition:
    workflow = ImperativeWorkflowDefinition(name)
    if data.get('description'):
        description = description_parser(data)
        workflow.set_description(description)
    if data.get('metadata'):
        for metadata_name, metadata_value in data.get('metadata'):
            workflow.add_metadata(Metadata(metadata_name, metadata_value))
    if data.get('inputs'):
        for input_property_name, input_property_value in data.get('inputs').items():
            workflow.add_inputs(property_definition_parser(input_property_name, input_property_value))
    if data.get('preconditions'):
        for prediction in data.get('predictions'):
            workflow.add_prediction(workflow_prediction_definition_parser(prediction))


    return workflow
