from werkzeug.exceptions import abort

from parser.parser.tosca_v_1_3.definitions.ParameterDefinition import parameter_definition_parser, ParameterDefinition


class CallOperationActivityDefinition:
    def __int__(self):
        self.operation = None
        self.vertex_type_system = 'CallOperationActivityDefinition'
        self.inputs = []


class DelegateWorkflowActivityDefinition:
    def __int__(self):
        self.workflow = None
        self.vertex_type_system = 'DelegateWorkflowActivityDefinition'
        self.inputs = []


class SetStateActivityDefinition:
    def __int__(self):
        self.set_state = None
        self.vertex_type_system = 'SetStateActivityDefinition'


class InlineWorkflowActivityDefinition:
    def __int__(self):
        self.workflow = None
        self.vertex_type_system = 'InlineWorkflowActivityDefinition'
        self.inputs = []


def activity_definition_parser(data: dict):
    for key_name in data.keys():
        if key_name == 'call_operation':
            call_operation = CallOperationActivityDefinition()
            if type(data[key_name]) == str:
                call_operation.operation = data[key_name]
            else:
                for call_operation_key, call_operation_value in data[key_name].items():
                    if call_operation_key == 'operation':
                        call_operation.operation = call_operation_value
                    if call_operation_key == 'inputs':
                        for input_def in call_operation_value:
                            for parameter_name, parameter_value in input_def.items():
                                call_operation.inputs.append(
                                    parameter_definition_parser(parameter_name, parameter_value))
        if key_name == 'delegate':
            delegate_workflow = DelegateWorkflowActivityDefinition()
            if type(data[key_name]) == str:
                delegate_workflow.workflow = data[key_name]
            else:
                for delegate_workflow_key, delegate_workflow_value in data[key_name].items():
                    if delegate_workflow_key == 'workflow':
                        delegate_workflow.workflow = delegate_workflow_value
                    if delegate_workflow_key == 'inputs':
                        for input_def in delegate_workflow_value:
                            for parameter_name, parameter_value in input_def.items():
                                delegate_workflow.inputs.append(
                                    parameter_definition_parser(parameter_name, parameter_value))
        if key_name == 'delegate':
            set_state = SetStateActivityDefinition()
            if type(data[key_name]) == str:
                set_state.set_state = data[key_name]
            else:
                abort(400)
        if key_name == 'inline':
            inline_workflow = InlineWorkflowActivityDefinition()
            if type(data[key_name]) == str:
                inline_workflow.workflow = data[key_name]
            else:
                for delegate_workflow_key, delegate_workflow_value in data[key_name].items():
                    if delegate_workflow_key == 'workflow':
                        inline_workflow.workflow = delegate_workflow_value
                    if delegate_workflow_key == 'inputs':
                        for input_def in delegate_workflow_value:
                            for parameter_name, parameter_value in input_def.items():
                                inline_workflow.inputs.append(
                                    parameter_definition_parser(parameter_name, parameter_value))
