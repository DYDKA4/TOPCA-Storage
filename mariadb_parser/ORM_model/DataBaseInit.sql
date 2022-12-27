create table artifact_storage
(
    id   int                          not null
        primary key,
    data longtext collate utf8mb4_bin not null,
    name char(32)                     not null
);

create table dependency_types
(
    source_id       int                                                           not null,
    dependency_id   int                                                           not null,
    dependency_type enum ('derived_from', 'requirement_dependency', 'dependency') not null,
    primary key (dependency_id, source_id),
    constraint type_dependency_types_type_table_id_fk
        foreign key (source_id) references type (id),
    constraint type_dependency_types_type_table_id_fk2
        foreign key (dependency_id) references type (id)
);

create index type_dependency_types_dependency_id_index
    on dependency_types (dependency_id);

create index type_dependency_types_source_id_index
    on dependency_types (source_id);

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

