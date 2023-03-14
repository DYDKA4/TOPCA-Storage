create table alembic_version
(
    version_num varchar(32) not null
        primary key
);

create table artifact_storage
(
    id   binary(36)                   not null
        primary key,
    name char(255)                    not null,
    data longtext collate utf8mb4_bin not null,
    constraint data
        check (json_valid(`data`))
);

create table instance_model
(
    id          binary(36)                   not null
        primary key,
    description text                         null,
    metadata    longtext collate utf8mb4_bin null,
    constraint metadata
        check (json_valid(`metadata`))
);

create table type
(
    id                        binary(36)                                                                                                                              not null
        primary key,
    version                   char(32)                                                                                                                                not null,
    type_of_type              enum ('artifact_type', 'data_type', 'capability_type', 'interface_type', 'relationship_type', 'node_type', 'group_type', 'policy_type') not null,
    type_name                 char(64)                                                                                                                                not null,
    data                      longtext collate utf8mb4_bin                                                                                                            not null,
    path_to_type              char(255)                                                                                                                               not null,
    tosca_definitions_version char(32)                                                                                                                                not null,
    constraint data
        check (json_valid(`data`))
);

create table dependency_types
(
    source_id       binary(36)                                                    not null,
    dependency_id   binary(36)                                                    not null,
    dependency_type enum ('derived_from', 'requirement_dependency', 'dependency') not null,
    primary key (source_id, dependency_type, dependency_id),
    constraint dependency_id
        foreign key (dependency_id) references type (id)
            on update cascade on delete cascade,
    constraint source_fk
        foreign key (source_id) references type (id)
            on update cascade on delete cascade
);

create table node_template
(
    id                binary(36)                   not null
        primary key,
    type_name         char(255)                    not null,
    type_id           binary(36)                   null,
    description       text                         null,
    metadata          longtext collate utf8mb4_bin null,
    copy_name         char(255)                    null,
    copy_id           binary(36)                   null,
    instance_model_id binary(36)                   not null,
    name              char(255)                    not null,
    constraint copy_fk
        foreign key (copy_id) references node_template (id),
    constraint instace_mode_if
        foreign key (instance_model_id) references instance_model (id),
    constraint node_type_fk
        foreign key (type_id) references type (id),
    constraint metadata
        check (json_valid(`metadata`))
);

create table capability
(
    id      binary(36)                   not null
        primary key,
    value   longtext collate utf8mb4_bin null,
    node_id binary(36)                   not null,
    constraint node_id
        foreign key (node_id) references node_template (id),
    constraint value
        check (json_valid(`value`))
);

create table node_interface
(
    id      binary(36) not null
        primary key,
    name    char(255)  not null,
    node_id binary(36) not null,
    constraint node_interface_node_template_null_fk
        foreign key (node_id) references node_template (id)
);

create table node_interface_operation
(
    id                binary(36)   not null
        primary key,
    name              varchar(255) not null,
    implementation    varchar(255) not null,
    node_interface_id binary(36)   not null,
    constraint node_interface_operation_node_interface_null_fk
        foreign key (node_interface_id) references node_interface (id)
);

create table requirement
(
    id         binary(36) not null
        primary key,
    capability char(255)  null,
    name       char(255)  not null,
    node_id    binary(36) not null,
    node       char(255)  not null,
    node_link  binary(36) not null,
    constraint requirement_node_template_null_fk
        foreign key (node_id) references node_template (id),
    constraint requirement_node_template_null_fk2
        foreign key (node_link) references node_template (id)
);

create table relationship_interface
(
    id             binary(36) not null
        primary key,
    name           char(255)  not null,
    requirement_id binary(36) not null,
    constraint relationship_interface_requirement_fk
        foreign key (requirement_id) references requirement (id)
);

create table relationship_interface_operation
(
    id                        binary(36)   not null
        primary key,
    name                      varchar(255) not null,
    implementation            varchar(255) not null,
    relationship_interface_id binary(36)   not null,
    constraint relationship_interface_operation_relationship_interface_fk
        foreign key (relationship_interface_id) references relationship_interface (id)
);

create table ts_to_as
(
    artifact_storage_id binary(36) not null,
    type_storage_id     binary(36) not null,
    primary key (artifact_storage_id, type_storage_id),
    constraint foreign_key_name
        foreign key (artifact_storage_id) references artifact_storage (id)
            on update cascade on delete cascade,
    constraint ts_to_as_type_null_fk
        foreign key (type_storage_id) references type (id)
            on update cascade on delete cascade
);

create table value_storage
(
    id    binary(36)                   not null
        primary key,
    value longtext collate utf8mb4_bin null,
    constraint value
        check (json_valid(`value`))
);

create table capability_attribute_and_property
(
    id               binary(36)                     not null
        primary key,
    name             char(255)                      not null,
    value_storage_id binary(36)                     not null,
    capability_id    binary(36)                     not null,
    type             enum ('attribute', 'property') not null,
    constraint capability_attribute_and_property_value_storage_null_fk
        foreign key (value_storage_id) references value_storage (id),
    constraint capability_fk
        foreign key (capability_id) references capability (id)
);

create table im_input_and_output
(
    id                binary(36)                   not null
        primary key,
    instance_model_id binary(36)                   not null,
    key_schema        longtext collate utf8mb4_bin null,
    type_name         char(255)                    not null,
    type_id           binary(36)                   null,
    description       text                         null,
    required          tinyint(1)                   null,
    `default`         longtext collate utf8mb4_bin null,
    entry_schema      longtext collate utf8mb4_bin null,
    type              enum ('input', 'output')     not null,
    mapping           longtext collate utf8mb4_bin null,
    value_storage_id  binary(36)                   not null,
    name              char(255)                    not null,
    constraint data_type_fk
        foreign key (type_id) references type (id)
            on update cascade,
    constraint instance_model_id_fk
        foreign key (instance_model_id) references instance_model (id)
            on update cascade on delete cascade,
    constraint value_storage_fk
        foreign key (value_storage_id) references value_storage (id)
            on update cascade on delete cascade,
    constraint `default`
        check (json_valid(`default`)),
    constraint entry_schema
        check (json_valid(`entry_schema`)),
    constraint key_schema
        check (json_valid(`key_schema`)),
    constraint mapping
        check (json_valid(`mapping`))
);

create table node_attribute_and_property
(
    id               binary(36)                     not null
        primary key,
    name             char(255)                      not null,
    type             enum ('attribute', 'property') not null,
    value_storage_id binary(36)                     not null,
    node_id          binary(36)                     not null,
    constraint Node_fk
        foreign key (node_id) references node_template (id)
            on update cascade on delete cascade,
    constraint value_stoarge_fk
        foreign key (value_storage_id) references value_storage (id)
            on update cascade on delete cascade
);

create table node_interface_operation_input_output
(
    id               binary(36)               not null
        primary key,
    name             char(255)                not null,
    value_storage_id binary(36)               not null,
    operation_id     binary(36)               not null,
    type             enum ('input', 'output') not null,
    constraint interface_operation_fk
        foreign key (operation_id) references node_interface_operation (id),
    constraint node_interface_operation_input_output_value_storage_fk
        foreign key (value_storage_id) references value_storage (id)
);

create table relationship_attribute_and_property
(
    id               binary(36)                     not null
        primary key,
    name             char(255)                      not null,
    type             enum ('attribute', 'property') not null,
    value_storage_id binary(36)                     not null,
    requirement_id   binary(36)                     not null,
    constraint relationship_attribute_and_property_requirement_fk
        foreign key (requirement_id) references requirement (id)
            on update cascade on delete cascade,
    constraint relationship_attribute_and_property_value_storage_fk
        foreign key (value_storage_id) references value_storage (id)
            on update cascade on delete cascade
);

create table relationship_interface_operation_input_output
(
    id               binary(36)               not null
        primary key,
    name             char(255)                not null,
    value_storage_id binary(36)               not null,
    operation_id     binary(36)               not null,
    type             enum ('input', 'output') not null,
    constraint relationship_interface_operation_input_output_operation_fk
        foreign key (operation_id) references relationship_interface_operation (id),
    constraint relationship_interface_operation_input_output_value_storage_fk
        foreign key (value_storage_id) references value_storage (id)
);

