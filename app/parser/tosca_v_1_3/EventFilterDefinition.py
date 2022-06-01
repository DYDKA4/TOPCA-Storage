# node: <node_type_name> | <node_template_name>
# requirement: <requirement_name>
# capability: <capability_name>

class EventFilterDefinition:
    def __init__(self, node: str, requirement: str = None, capability: str = None):
        self.vid = None
        self.node = node
        self.requirement = requirement
        self.capability = capability
        self.vertex_type_system = 'EventFilterDefinition'
