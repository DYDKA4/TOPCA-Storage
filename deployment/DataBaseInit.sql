create table TOPCA_storage.alembic_version
(
    version_num varchar(32) not null
        primary key
);

create table TOPCA_storage.artifact_storage
(
    id   char(36)                     not null
        primary key,
    name char(255)                    not null,
    data longtext collate utf8mb4_bin not null,
    constraint data
        check (json_valid(`data`))
);

create table TOPCA_storage.instance_model
(
    id          char(36)                     not null
        primary key,
    description text                         null,
    metadata    longtext collate utf8mb4_bin null,
    constraint metadata
        check (json_valid(`metadata`))
);

create table TOPCA_storage.type_header
(
    id                        char(36)                     not null
        primary key,
    template_version          char(255)                    not null,
    template_name             char(255)                    not null,
    tosca_definitions_version char(255)                    not null,
    metadata                  longtext collate utf8mb4_bin null,
    template_author           char(255)                    not null,
    imports                   longtext collate utf8mb4_bin null,
    constraint type_header_complex_pk
        unique (template_name, template_author, template_version, tosca_definitions_version) using hash,
    constraint imports
        check (json_valid(`imports`)),
    constraint metadata
        check (json_valid(`metadata`))
);

create table TOPCA_storage.type
(
    id           char(36)                                                                                                                                not null
        primary key,
    version      char(32)                                                                                                                                null,
    type_of_type enum ('artifact_type', 'data_type', 'capability_type', 'interface_type', 'relationship_type', 'node_type', 'group_type', 'policy_type') not null,
    type_name    char(64)                                                                                                                                not null,
    data         longtext collate utf8mb4_bin                                                                                                            not null,
    header_id    char(36)                                                                                                                                not null,
    constraint type_type_header_null_fk
        foreign key (header_id) references TOPCA_storage.type_header (id)
            on update cascade on delete cascade,
    constraint data
        check (json_valid(`data`))
);

create table TOPCA_storage.dependency_types
(
    source_id       char(36)                                                      not null,
    dependency_id   char(36)                                                      not null,
    dependency_type enum ('derived_from', 'requirement_dependency', 'dependency') not null,
    primary key (source_id, dependency_type, dependency_id),
    constraint dependency_id
        foreign key (dependency_id) references TOPCA_storage.type (id)
            on update cascade on delete cascade,
    constraint source_fk
        foreign key (source_id) references TOPCA_storage.type (id)
            on update cascade on delete cascade
);

create table TOPCA_storage.node_template
(
    id                char(36)                     not null
        primary key,
    type_name         char(255)                    not null,
    type_id           char(36)                     null,
    description       text                         null,
    metadata          longtext collate utf8mb4_bin null,
    copy_name         char(255)                    null,
    copy_id           char(36)                     null,
    instance_model_id char(36)                     not null,
    name              char(255)                    not null,
    directives        longtext collate utf8mb4_bin null,
    constraint copy_fk
        foreign key (copy_id) references TOPCA_storage.node_template (id),
    constraint instace_mode_if
        foreign key (instance_model_id) references TOPCA_storage.instance_model (id)
            on update cascade on delete cascade,
    constraint node_type_fk
        foreign key (type_id) references TOPCA_storage.type (id),
    constraint directives
        check (json_valid(`directives`)),
    constraint metadata
        check (json_valid(`metadata`))
);

create table TOPCA_storage.capability
(
    id      char(36)                     not null
        primary key,
    value   longtext collate utf8mb4_bin null,
    node_id char(36)                     not null,
    name    char(255)                    not null,
    type    char(255)                    null,
    constraint node_id
        foreign key (node_id) references TOPCA_storage.node_template (id)
            on update cascade on delete cascade,
    constraint value
        check (json_valid(`value`))
);

create table TOPCA_storage.node_interface
(
    id      char(36)  not null
        primary key,
    name    char(255) not null,
    node_id char(36)  not null,
    type    char(255) not null,
    constraint node_interface_node_template_null_fk
        foreign key (node_id) references TOPCA_storage.node_template (id)
            on update cascade on delete cascade
);

create table TOPCA_storage.node_interface_operation
(
    id                char(36)                     not null
        primary key,
    name              varchar(255)                 not null,
    implementation    longtext collate utf8mb4_bin null,
    node_interface_id char(36)                     not null,
    constraint node_interface_operation_node_interface_null_fk
        foreign key (node_interface_id) references TOPCA_storage.node_interface (id)
            on update cascade on delete cascade,
    constraint implementation
        check (json_valid(`implementation`))
);

create table TOPCA_storage.requirement
(
    id                char(36)  not null
        primary key,
    capability        char(255) null,
    name              char(255) not null,
    node_id           char(36)  not null,
    node              char(255) null,
    node_link         char(36)  null,
    relationship_type char(255) not null,
    `order`           int       not null,
    constraint requirement_node_template_id_fk_2
        foreign key (node_link) references TOPCA_storage.node_template (id)
            on update cascade on delete cascade,
    constraint requirement_node_template_null_fk
        foreign key (node_id) references TOPCA_storage.node_template (id)
            on update cascade on delete cascade
);

create table TOPCA_storage.relationship_interface
(
    id             char(36)  not null
        primary key,
    name           char(255) not null,
    requirement_id char(36)  not null,
    type           char(255) not null,
    constraint relationship_interface_requirement_fk
        foreign key (requirement_id) references TOPCA_storage.requirement (id)
            on update cascade on delete cascade
);

create table TOPCA_storage.relationship_interface_operation
(
    id                        char(36)     not null
        primary key,
    name                      varchar(255) not null,
    implementation            varchar(255) null,
    relationship_interface_id char(36)     not null,
    constraint relationship_interface_operation_relationship_interface_fk
        foreign key (relationship_interface_id) references TOPCA_storage.relationship_interface (id)
            on update cascade on delete cascade
);

create table TOPCA_storage.ts_to_as
(
    artifact_storage_id char(36) not null,
    type_storage_id     char(36) not null,
    primary key (artifact_storage_id, type_storage_id),
    constraint foreign_key_name
        foreign key (artifact_storage_id) references TOPCA_storage.artifact_storage (id)
            on update cascade on delete cascade,
    constraint ts_to_as_type_null_fk
        foreign key (type_storage_id) references TOPCA_storage.type (id)
            on update cascade on delete cascade
);

create table TOPCA_storage.value_storage
(
    id    char(36)                     not null
        primary key,
    value longtext collate utf8mb4_bin null,
    constraint value
        check (json_valid(`value`))
);

create table TOPCA_storage.capability_attribute_and_property
(
    id               char(36)                       not null
        primary key,
    name             char(255)                      not null,
    value_storage_id char(36)                       not null,
    capability_id    char(36)                       not null,
    type             enum ('attribute', 'property') not null,
    constraint capability_attribute_and_property_value_storage_null_fk
        foreign key (value_storage_id) references TOPCA_storage.value_storage (id),
    constraint capability_fk
        foreign key (capability_id) references TOPCA_storage.capability (id)
            on update cascade on delete cascade
);

create table TOPCA_storage.instance_model_input_and_output
(
    id                char(36)                     not null
        primary key,
    instance_model_id char(36)                     not null,
    key_schema        longtext collate utf8mb4_bin null,
    type_name         char(255)                    null,
    type_id           char(36)                     null,
    description       text                         null,
    required          tinyint(1)                   null,
    `default`         longtext collate utf8mb4_bin null,
    entry_schema      longtext collate utf8mb4_bin null,
    type              enum ('input', 'output')     not null,
    mapping           longtext collate utf8mb4_bin null,
    value_storage_id  char(36)                     not null,
    name              char(255)                    not null,
    constraint data_type_fk
        foreign key (type_id) references TOPCA_storage.type (id)
            on update cascade,
    constraint instance_model_id_fk
        foreign key (instance_model_id) references TOPCA_storage.instance_model (id)
            on update cascade on delete cascade,
    constraint value_storage_fk
        foreign key (value_storage_id) references TOPCA_storage.value_storage (id)
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

create table TOPCA_storage.node_attribute_and_property
(
    id               char(36)                       not null
        primary key,
    name             char(255)                      not null,
    type             enum ('attribute', 'property') not null,
    value_storage_id char(36)                       not null,
    node_id          char(36)                       not null,
    constraint Node_fk
        foreign key (node_id) references TOPCA_storage.node_template (id)
            on update cascade on delete cascade,
    constraint value_stoarge_fk
        foreign key (value_storage_id) references TOPCA_storage.value_storage (id)
            on update cascade on delete cascade
);

create table TOPCA_storage.node_interface_operation_input_output
(
    id               char(36)                 not null
        primary key,
    name             char(255)                not null,
    value_storage_id char(36)                 not null,
    operation_id     char(36)                 not null,
    type             enum ('input', 'output') not null,
    constraint interface_operation_fk
        foreign key (operation_id) references TOPCA_storage.node_interface_operation (id)
            on update cascade on delete cascade,
    constraint node_interface_operation_input_output_value_storage_fk
        foreign key (value_storage_id) references TOPCA_storage.value_storage (id)
);

create table TOPCA_storage.relationship_attribute_and_property
(
    id               char(36)                       not null
        primary key,
    name             char(255)                      not null,
    type             enum ('attribute', 'property') not null,
    value_storage_id char(36)                       not null,
    requirement_id   char(36)                       not null,
    constraint relationship_attribute_and_property_requirement_fk
        foreign key (requirement_id) references TOPCA_storage.requirement (id)
            on update cascade on delete cascade,
    constraint relationship_attribute_and_property_value_storage_fk
        foreign key (value_storage_id) references TOPCA_storage.value_storage (id)
            on update cascade on delete cascade
);

create table TOPCA_storage.relationship_interface_operation_input_output
(
    id               char(36)                 not null
        primary key,
    name             char(255)                not null,
    value_storage_id char(36)                 not null,
    operation_id     char(36)                 not null,
    type             enum ('input', 'output') not null,
    constraint relationship_interface_operation_input_output_operation_fk
        foreign key (operation_id) references TOPCA_storage.relationship_interface_operation (id)
            on update cascade on delete cascade,
    constraint relationship_interface_operation_input_output_value_storage_fk
        foreign key (value_storage_id) references TOPCA_storage.value_storage (id)
);

