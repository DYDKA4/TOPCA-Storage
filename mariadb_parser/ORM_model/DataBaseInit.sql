create table alembic_version
(
    version_num varchar(32) not null
        primary key
);

create table artifact_storage
(
    id   int                          not null
        primary key,
    data longtext collate utf8mb4_bin not null,
    name char(32)                     not null
);

create table instance_model
(
    description text                         null,
    id          int                          not null
        primary key,
    metadata    longtext collate utf8mb4_bin null,
    constraint metadata
        check (json_valid(`metadata`))
);

create table type
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

create table dependency_types
(
    source_id       int                                                           not null,
    dependency_id   int                                                           not null,
    dependency_type enum ('derived_from', 'requirement_dependency', 'dependency') not null,
    primary key (dependency_id, source_id, dependency_type),
    constraint type_dependency_types_type_table_id_fk
        foreign key (source_id) references type (id)
            on delete cascade,
    constraint type_dependency_types_type_table_id_fk2
        foreign key (dependency_id) references type (id)
            on delete cascade
);

create index type_dependency_types_dependency_id_index
    on dependency_types (dependency_id);

create index type_dependency_types_source_id_index
    on dependency_types (source_id);

create table node
(
    id               int                          not null
        primary key,
    instance_mode_id int                          not null,
    name             char(32)                     not null,
    type_id          int                          not null,
    description      text                         null,
    metadata         longtext collate utf8mb4_bin null,
    copy             int                          null,
    subsistitute     int                          null,
    constraint foreign_key_name
        foreign key (subsistitute) references instance_model (id),
    constraint node_template_instance_model_null_fk
        foreign key (instance_mode_id) references instance_model (id),
    constraint node_template_node_template_id_fk
        foreign key (copy) references node (id),
    constraint node_template_type_null_fk
        foreign key (type_id) references type (id),
    constraint metadata
        check (json_valid(`metadata`))
);

create table capability
(
    id      int                          not null
        primary key,
    node_id int                          not null,
    name    char(32)                     not null,
    value   longtext collate utf8mb4_bin null,
    constraint capability_node_template_null_fk
        foreign key (node_id) references node (id),
    constraint value
        check (json_valid(`value`))
);

create table interface_from_node_template
(
    id             int                          not null
        primary key,
    node_id        int                          not null,
    implementation longtext collate utf8mb4_bin null,
    name           char(32)                     not null,
    constraint interface_from_node_template_node_template_null_fk
        foreign key (node_id) references node (id),
    constraint implementation
        check (json_valid(`implementation`))
);

create table node_to_artifact_storage
(
    node_id             int not null,
    artifact_storage_id int not null,
    primary key (artifact_storage_id, node_id),
    constraint node_template_to_artifact_storage_artifact_storage_null_fk
        foreign key (artifact_storage_id) references artifact_storage (id),
    constraint node_template_to_artifact_storage_node_template_null_fk
        foreign key (node_id) references node (id)
);

create table relationship
(
    id                int                          not null
        primary key,
    name              char(32)                     not null,
    instance_model_id int                          not null,
    descriptiom       text                         null,
    metadata          longtext collate utf8mb4_bin not null,
    copy              int                          null,
    type_id           int                          not null,
    constraint relationship_template_instance_model_null_fk
        foreign key (instance_model_id) references instance_model (id),
    constraint relationship_template_relationship_template_id_fk
        foreign key (copy) references relationship (id),
    constraint relationship_template_type_null_fk
        foreign key (type_id) references type (id),
    constraint metadata
        check (json_valid(`metadata`))
);

create table relationships_interface
(
    id              int                          not null
        primary key,
    relationship_id int                          not null,
    implementation  longtext collate utf8mb4_bin not null,
    constraint relationships_interface_relationship_template_null_fk
        foreign key (relationship_id) references relationship (id),
    constraint implementation
        check (json_valid(`implementation`))
);

create table requirement
(
    id              int                          not null
        primary key,
    name            char(32)                     not null,
    target_node_id  int                          null,
    node_filter     longtext collate utf8mb4_bin null,
    node_id         int                          not null,
    value           longtext collate utf8mb4_bin null,
    relationship_id int                          null,
    constraint requirement_node_template_id_fk
        foreign key (target_node_id) references node (id),
    constraint requirement_node_template_null_fk
        foreign key (node_id) references node (id),
    constraint requirement_relationship_null_fk
        foreign key (relationship_id) references relationship (id),
    constraint node_filter
        check (json_valid(`node_filter`)),
    constraint value
        check (json_valid(`value`))
);

create table type_storage_to_artifact_storage
(
    artifact_storage_id int not null,
    type_storage_id     int not null,
    primary key (artifact_storage_id, type_storage_id),
    constraint type_storage_to_artifact_storage_artifact_storage_id_fk
        foreign key (artifact_storage_id) references artifact_storage (id),
    constraint type_storage_to_artifact_storage_type_storage_id_fk
        foreign key (type_storage_id) references type (id)
);

create table value_storage
(
    id   int                          not null
        primary key,
    data longtext collate utf8mb4_bin not null,
    constraint data
        check (json_valid(`data`))
);

create table attribute_and_property_from_capability
(
    id               int                            not null
        primary key,
    capability_id    int                            not null,
    type             enum ('attribute', 'property') not null,
    value_storage_id int                            not null,
    name             char(32)                       not null,
    constraint attribute_and_property_from_capability_capability_null_fk
        foreign key (capability_id) references capability (id),
    constraint attribute_and_property_from_capability_value_storage_null_fk
        foreign key (value_storage_id) references value_storage (id)
);

create table attribute_and_property_from_node
(
    id               int                            not null
        primary key,
    node_id          int                            not null,
    type             enum ('attribute', 'property') not null,
    value_storage_id int                            not null,
    name             char(32)                       not null,
    constraint attribute_and_property_from_node_template_node_template_id_fk
        foreign key (node_id) references node (id),
    constraint attribute_and_property_from_node_template_value_storage_null_fk
        foreign key (value_storage_id) references value_storage (id)
);

create table get_functions
(
    source_id int not null,
    target_id int not null,
    primary key (source_id, target_id),
    constraint get_functions_value_storage_fk
        foreign key (target_id) references value_storage (id),
    constraint get_functions_value_storage_null_fk
        foreign key (source_id) references value_storage (id)
);

create table input_and_output_from_instance_model
(
    id               int                      not null
        primary key,
    instance_mode_id int                      not null,
    type             enum ('input', 'output') not null,
    value_storage_id int                      not null,
    constraint inputs_and_output_from_instance_model_instance_model_null_fk
        foreign key (instance_mode_id) references instance_model (id),
    constraint inputs_and_output_from_instance_model_value_storage_null_fk
        foreign key (value_storage_id) references value_storage (id)
);

create table input_from_interface_in_node
(
    id               int not null
        primary key,
    father_node_id   int not null,
    value_storage_id int not null,
    constraint iofint_fk_to_data_storage
        foreign key (value_storage_id) references value_storage (id),
    constraint iofint_fk_to_interface_node
        foreign key (father_node_id) references interface_from_node_template (id)
);

create table interfaces_input_from_relationship
(
    id               int not null
        primary key,
    interface_id     int not null,
    value_storage_id int not null,
    constraint inputs_from_relationship_value_storage_null_fk
        foreign key (value_storage_id) references value_storage (id),
    constraint nputs_from_relationship_relationships_interface_null_fk
        foreign key (interface_id) references relationships_interface (id)
);

create table relationships_property_and_attribute
(
    id               int                            not null
        primary key,
    type             enum ('property', 'attribute') not null,
    relationship_id  int                            not null,
    value_storage_id int                            not null,
    name             char(32)                       not null,
    constraint property_and_attribute_relationship_template_null_fk
        foreign key (relationship_id) references relationship (id),
    constraint relationships_property_and_attribute_value_storage_null_fk
        foreign key (value_storage_id) references value_storage (id)
);

