create table topca_storage.artifact_storage
(
    id   int                          not null
        primary key,
    data longtext collate utf8mb4_bin not null,
    name char(32)                     not null
);

create table topca_storage.topology_template_definition
(
    id                        int                          not null
        primary key,
    description               text                         null,
    substitution_mappings     longtext collate utf8mb4_bin null,
    tosca_definitions_version text                         null,
    metadata                  longtext collate utf8mb4_bin null,
    namespace                 text                         null,
    STD_description           text                         null,
    repositories              longtext collate utf8mb4_bin null,
    imports                   longtext collate utf8mb4_bin null,
    constraint imports
        check (json_valid(`imports`)),
    constraint metadata
        check (json_valid(`metadata`)),
    constraint repositories
        check (json_valid(`repositories`)),
    constraint substitution_mappings
        check (json_valid(`substitution_mappings`))
);

create table topca_storage.inputs
(
    id     int                          not null
        primary key,
    ttd_id int                          not null,
    name   char(32)                     not null,
    data   longtext collate utf8mb4_bin null,
    constraint inputs_topology_template_definition_null_fk
        foreign key (ttd_id) references topca_storage.topology_template_definition (id)
            on delete cascade,
    constraint data
        check (json_valid(`data`))
);

create table topca_storage.relationship_templates
(
    id     int                          not null
        primary key,
    ttd_id int                          not null,
    name   char(32)                     not null,
    data   longtext collate utf8mb4_bin null,
    constraint Relationship_Templates_topology_template_definition_null_fk
        foreign key (ttd_id) references topca_storage.topology_template_definition (id),
    constraint data
        check (json_valid(`data`))
);

create table topca_storage.type
(
    id           int                                                                                                                                     not null
        primary key,
    version      char(32)                                                                                                                                not null,
    type_of_type enum ('artifact_type', 'data_type', 'capability_type', 'interface_type', 'relationship_type', 'node_type', 'group_type', 'policy_type') not null,
    type_name    char(64)                                                                                                                                not null,
    data         longtext collate utf8mb4_bin                                                                                                            not null,
    constraint data
        check (json_valid(`data`))
);

create table topca_storage.dependency_types
(
    source_id       int                                                           not null,
    dependency_id   int                                                           not null,
    dependency_type enum ('derived_from', 'requirement_dependency', 'dependency') not null,
    primary key (dependency_id, source_id),
    constraint type_dependency_types_type_table_id_fk
        foreign key (source_id) references topca_storage.type (id),
    constraint type_dependency_types_type_table_id_fk2
        foreign key (dependency_id) references topca_storage.type (id)
);

create index type_dependency_types_dependency_id_index
    on topca_storage.dependency_types (dependency_id);

create index type_dependency_types_source_id_index
    on topca_storage.dependency_types (source_id);

create table topca_storage.node_template
(
    id      int                          not null
        primary key,
    ttd_id  int                          not null,
    name    char(32)                     not null,
    data    longtext collate utf8mb4_bin null,
    type_id int                          not null,
    constraint node_template_topology_template_definition_null_fk
        foreign key (ttd_id) references topca_storage.topology_template_definition (id)
            on delete cascade,
    constraint node_template_type_null_fk
        foreign key (type_id) references topca_storage.type (id),
    constraint data
        check (json_valid(`data`))
);

create table topca_storage.attribute
(
    id                int                          not null
        primary key,
    node_templates_id int                          not null,
    name              char(32)                     not null,
    data              longtext collate utf8mb4_bin not null,
    constraint attribute_node_template_null_fk
        foreign key (node_templates_id) references topca_storage.node_template (id)
            on delete cascade,
    constraint data
        check (json_valid(`data`))
);

create table topca_storage.capability
(
    id               int                                                                                          not null
        primary key,
    father_node_id   int                                                                                          not null,
    father_node_type enum ('Inputs', 'NodeTemplates', 'RelationshipTemplates', ' Groups', 'Policies', 'Workflow') not null,
    name             char(32)                                                                                     not null,
    data             longtext collate utf8mb4_bin                                                                 null,
    constraint capability_node_template_null_fk
        foreign key (father_node_id) references topca_storage.node_template (id),
    constraint data
        check (json_valid(`data`))
);

create table topca_storage.property
(
    id               int                                                                                          not null
        primary key,
    father_node_id   int                                                                                          not null,
    father_node_type enum ('Inputs', 'NodeTemplates', 'RelationshipTemplates', ' Groups', 'Policies', 'Workflow') not null,
    data             longtext collate utf8mb4_bin                                                                 null,
    constraint property_node_template_null_fk
        foreign key (father_node_id) references topca_storage.node_template (id),
    constraint foreign_key_name
        foreign key (father_node_id) references topca_storage.capability (id),
    constraint data
        check (json_valid(`data`))
);

create table topca_storage.get_functions
(
    source_id   int                                                                                         not null,
    source_type enum ('Inputs', 'NodeTemplates', 'RelationshipTemplates', 'Groups', 'Policies', 'Workflow') not null,
    target_id   int                                                                                         not null,
    target_type enum ('Inputs', 'NodeTemplates', 'RelationshipTemplates', 'Groups', 'Policies', 'Workflow') not null,
    primary key (source_id, source_type, target_id, target_type),
    constraint GetFunctions_property_source
        foreign key (source_id) references topca_storage.property (id),
    constraint GetFunctions_property_target
        foreign key (target_id) references topca_storage.property (id),
    constraint get_functions_inputs_source
        foreign key (source_id) references topca_storage.inputs (id),
    constraint get_functions_inputs_target
        foreign key (target_id) references topca_storage.inputs (id)
);

create table topca_storage.requirement
(
    id               int                          not null
        primary key,
    node_template_id int                          not null,
    name_id          int                          not null,
    data             longtext collate utf8mb4_bin not null,
    constraint Requirement_node_template_null_fk
        foreign key (node_template_id) references topca_storage.node_template (id)
            on delete cascade,
    constraint data
        check (json_valid(`data`))
);

create table topca_storage.node_filter
(
    source_id   int                                                                                         not null,
    target_id   int                                                                                         not null,
    source_type enum ('Inputs', 'NodeTemplates', 'RelationshipTemplates', 'Groups', 'Policies', 'Workflow') not null,
    target_type enum ('Inputs', 'NodeTemplates', 'RelationshipTemplates', 'Groups', 'Policies', 'Workflow') not null,
    primary key (target_id, source_id, source_type, target_type),
    constraint node_filter_node_template_null_fk
        foreign key (target_id) references topca_storage.node_template (id),
    constraint node_filter_requirement_null_fk
        foreign key (source_id) references topca_storage.requirement (id)
);

create table topca_storage.type_storage_to_artifact_storage
(
    artifact_storage_id int not null,
    type_storage_id     int not null,
    primary key (artifact_storage_id, type_storage_id),
    constraint type_storage_to_artifact_storage_artifact_storage_id_fk
        foreign key (artifact_storage_id) references topca_storage.artifact_storage (id),
    constraint type_storage_to_artifact_storage_type_storage_id_fk
        foreign key (type_storage_id) references topca_storage.type (id)
);

