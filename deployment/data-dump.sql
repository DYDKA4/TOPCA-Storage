-- MariaDB dump 10.19  Distrib 10.11.2-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: TOPCA_storage
-- ------------------------------------------------------
-- Server version	10.11.2-MariaDB-1:10.11.2+maria~ubu2204

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artifact_storage`
--

DROP TABLE IF EXISTS `artifact_storage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `artifact_storage` (
  `id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  `data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `data` CHECK (json_valid(`data`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artifact_storage`
--

LOCK TABLES `artifact_storage` WRITE;
/*!40000 ALTER TABLE `artifact_storage` DISABLE KEYS */;
/*!40000 ALTER TABLE `artifact_storage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `capability`
--

DROP TABLE IF EXISTS `capability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `capability` (
  `id` char(36) NOT NULL,
  `value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `node_id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  `type` char(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `node_id` (`node_id`),
  CONSTRAINT `node_id` FOREIGN KEY (`node_id`) REFERENCES `node_template` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `value` CHECK (json_valid(`value`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `capability`
--

LOCK TABLES `capability` WRITE;
/*!40000 ALTER TABLE `capability` DISABLE KEYS */;
/*!40000 ALTER TABLE `capability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `capability_attribute_and_property`
--

DROP TABLE IF EXISTS `capability_attribute_and_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `capability_attribute_and_property` (
  `id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  `value_storage_id` char(36) NOT NULL,
  `capability_id` char(36) NOT NULL,
  `type` enum('attribute','property') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `capability_attribute_and_property_value_storage_null_fk` (`value_storage_id`),
  KEY `capability_fk` (`capability_id`),
  CONSTRAINT `capability_attribute_and_property_value_storage_null_fk` FOREIGN KEY (`value_storage_id`) REFERENCES `value_storage` (`id`),
  CONSTRAINT `capability_fk` FOREIGN KEY (`capability_id`) REFERENCES `capability` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `capability_attribute_and_property`
--

LOCK TABLES `capability_attribute_and_property` WRITE;
/*!40000 ALTER TABLE `capability_attribute_and_property` DISABLE KEYS */;
/*!40000 ALTER TABLE `capability_attribute_and_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dependency_types`
--

DROP TABLE IF EXISTS `dependency_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dependency_types` (
  `source_id` char(36) NOT NULL,
  `dependency_id` char(36) NOT NULL,
  `dependency_type` enum('derived_from','requirement_dependency','dependency') NOT NULL,
  PRIMARY KEY (`source_id`,`dependency_type`,`dependency_id`),
  KEY `dependency_id` (`dependency_id`),
  CONSTRAINT `dependency_id` FOREIGN KEY (`dependency_id`) REFERENCES `type` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `source_fk` FOREIGN KEY (`source_id`) REFERENCES `type` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dependency_types`
--

LOCK TABLES `dependency_types` WRITE;
/*!40000 ALTER TABLE `dependency_types` DISABLE KEYS */;
/*!40000 ALTER TABLE `dependency_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instance_model`
--

DROP TABLE IF EXISTS `instance_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `instance_model` (
  `id` char(36) NOT NULL,
  `description` text DEFAULT NULL,
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `metadata` CHECK (json_valid(`metadata`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instance_model`
--

LOCK TABLES `instance_model` WRITE;
/*!40000 ALTER TABLE `instance_model` DISABLE KEYS */;
INSERT INTO `instance_model` VALUES
('78a4bd85-67eb-4f55-bf77-45c8a00e68d5',NULL,'{\"puccini.quirks\": \"imports.implicit.disable,namespace.normative.shortcuts.disable\", \"template_author\": \"sadimer\", \"template_name\": \"ray-master\", \"template_version\": \"1.0.0\"}'),
('87821a58-4e48-4acc-bb22-384146e2c8ef',NULL,'{\"puccini.quirks\": \"imports.implicit.disable,namespace.normative.shortcuts.disable\", \"template_author\": \"sadimer\", \"template_name\": \"ray-master\", \"template_version\": \"1.0.0\"}');
/*!40000 ALTER TABLE `instance_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instance_model_input_and_output`
--

DROP TABLE IF EXISTS `instance_model_input_and_output`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `instance_model_input_and_output` (
  `id` char(36) NOT NULL,
  `instance_model_id` char(36) NOT NULL,
  `key_schema` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `type_name` char(255) DEFAULT NULL,
  `type_id` char(36) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `required` tinyint(1) DEFAULT NULL,
  `default` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `entry_schema` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `type` enum('input','output') NOT NULL,
  `mapping` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `value_storage_id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `data_type_fk` (`type_id`),
  KEY `instance_model_id_fk` (`instance_model_id`),
  KEY `value_storage_fk` (`value_storage_id`),
  CONSTRAINT `data_type_fk` FOREIGN KEY (`type_id`) REFERENCES `type` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `instance_model_id_fk` FOREIGN KEY (`instance_model_id`) REFERENCES `instance_model` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `value_storage_fk` FOREIGN KEY (`value_storage_id`) REFERENCES `value_storage` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `default` CHECK (json_valid(`default`)),
  CONSTRAINT `entry_schema` CHECK (json_valid(`entry_schema`)),
  CONSTRAINT `key_schema` CHECK (json_valid(`key_schema`)),
  CONSTRAINT `mapping` CHECK (json_valid(`mapping`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instance_model_input_and_output`
--

LOCK TABLES `instance_model_input_and_output` WRITE;
/*!40000 ALTER TABLE `instance_model_input_and_output` DISABLE KEYS */;
/*!40000 ALTER TABLE `instance_model_input_and_output` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `node_attribute_and_property`
--

DROP TABLE IF EXISTS `node_attribute_and_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `node_attribute_and_property` (
  `id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  `type` enum('attribute','property') NOT NULL,
  `value_storage_id` char(36) NOT NULL,
  `node_id` char(36) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Node_fk` (`node_id`),
  KEY `value_stoarge_fk` (`value_storage_id`),
  CONSTRAINT `Node_fk` FOREIGN KEY (`node_id`) REFERENCES `node_template` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `value_stoarge_fk` FOREIGN KEY (`value_storage_id`) REFERENCES `value_storage` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `node_attribute_and_property`
--

LOCK TABLES `node_attribute_and_property` WRITE;
/*!40000 ALTER TABLE `node_attribute_and_property` DISABLE KEYS */;
/*!40000 ALTER TABLE `node_attribute_and_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `node_interface`
--

DROP TABLE IF EXISTS `node_interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `node_interface` (
  `id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  `node_id` char(36) NOT NULL,
  `type` char(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `node_interface_node_template_null_fk` (`node_id`),
  CONSTRAINT `node_interface_node_template_null_fk` FOREIGN KEY (`node_id`) REFERENCES `node_template` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `node_interface`
--

LOCK TABLES `node_interface` WRITE;
/*!40000 ALTER TABLE `node_interface` DISABLE KEYS */;
/*!40000 ALTER TABLE `node_interface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `node_interface_operation`
--

DROP TABLE IF EXISTS `node_interface_operation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `node_interface_operation` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `implementation` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `node_interface_id` char(36) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `node_interface_operation_node_interface_null_fk` (`node_interface_id`),
  CONSTRAINT `node_interface_operation_node_interface_null_fk` FOREIGN KEY (`node_interface_id`) REFERENCES `node_interface` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `implementation` CHECK (json_valid(`implementation`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `node_interface_operation`
--

LOCK TABLES `node_interface_operation` WRITE;
/*!40000 ALTER TABLE `node_interface_operation` DISABLE KEYS */;
/*!40000 ALTER TABLE `node_interface_operation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `node_interface_operation_input_output`
--

DROP TABLE IF EXISTS `node_interface_operation_input_output`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `node_interface_operation_input_output` (
  `id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  `value_storage_id` char(36) NOT NULL,
  `operation_id` char(36) NOT NULL,
  `type` enum('input','output') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `interface_operation_fk` (`operation_id`),
  KEY `node_interface_operation_input_output_value_storage_fk` (`value_storage_id`),
  CONSTRAINT `interface_operation_fk` FOREIGN KEY (`operation_id`) REFERENCES `node_interface_operation` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `node_interface_operation_input_output_value_storage_fk` FOREIGN KEY (`value_storage_id`) REFERENCES `value_storage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `node_interface_operation_input_output`
--

LOCK TABLES `node_interface_operation_input_output` WRITE;
/*!40000 ALTER TABLE `node_interface_operation_input_output` DISABLE KEYS */;
/*!40000 ALTER TABLE `node_interface_operation_input_output` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `node_template`
--

DROP TABLE IF EXISTS `node_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `node_template` (
  `id` char(36) NOT NULL,
  `type_name` char(255) NOT NULL,
  `type_id` char(36) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `copy_name` char(255) DEFAULT NULL,
  `copy_id` char(36) DEFAULT NULL,
  `instance_model_id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  `directives` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `copy_fk` (`copy_id`),
  KEY `instace_mode_if` (`instance_model_id`),
  KEY `node_type_fk` (`type_id`),
  CONSTRAINT `copy_fk` FOREIGN KEY (`copy_id`) REFERENCES `node_template` (`id`),
  CONSTRAINT `instace_mode_if` FOREIGN KEY (`instance_model_id`) REFERENCES `instance_model` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `node_type_fk` FOREIGN KEY (`type_id`) REFERENCES `type` (`id`),
  CONSTRAINT `directives` CHECK (json_valid(`directives`)),
  CONSTRAINT `metadata` CHECK (json_valid(`metadata`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `node_template`
--

LOCK TABLES `node_template` WRITE;
/*!40000 ALTER TABLE `node_template` DISABLE KEYS */;
/*!40000 ALTER TABLE `node_template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relationship_attribute_and_property`
--

DROP TABLE IF EXISTS `relationship_attribute_and_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relationship_attribute_and_property` (
  `id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  `type` enum('attribute','property') NOT NULL,
  `value_storage_id` char(36) NOT NULL,
  `requirement_id` char(36) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_attribute_and_property_requirement_fk` (`requirement_id`),
  KEY `relationship_attribute_and_property_value_storage_fk` (`value_storage_id`),
  CONSTRAINT `relationship_attribute_and_property_requirement_fk` FOREIGN KEY (`requirement_id`) REFERENCES `requirement` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relationship_attribute_and_property_value_storage_fk` FOREIGN KEY (`value_storage_id`) REFERENCES `value_storage` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationship_attribute_and_property`
--

LOCK TABLES `relationship_attribute_and_property` WRITE;
/*!40000 ALTER TABLE `relationship_attribute_and_property` DISABLE KEYS */;
/*!40000 ALTER TABLE `relationship_attribute_and_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relationship_interface`
--

DROP TABLE IF EXISTS `relationship_interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relationship_interface` (
  `id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  `requirement_id` char(36) NOT NULL,
  `type` char(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_interface_requirement_fk` (`requirement_id`),
  CONSTRAINT `relationship_interface_requirement_fk` FOREIGN KEY (`requirement_id`) REFERENCES `requirement` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationship_interface`
--

LOCK TABLES `relationship_interface` WRITE;
/*!40000 ALTER TABLE `relationship_interface` DISABLE KEYS */;
/*!40000 ALTER TABLE `relationship_interface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relationship_interface_operation`
--

DROP TABLE IF EXISTS `relationship_interface_operation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relationship_interface_operation` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `implementation` varchar(255) DEFAULT NULL,
  `relationship_interface_id` char(36) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_interface_operation_relationship_interface_fk` (`relationship_interface_id`),
  CONSTRAINT `relationship_interface_operation_relationship_interface_fk` FOREIGN KEY (`relationship_interface_id`) REFERENCES `relationship_interface` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationship_interface_operation`
--

LOCK TABLES `relationship_interface_operation` WRITE;
/*!40000 ALTER TABLE `relationship_interface_operation` DISABLE KEYS */;
/*!40000 ALTER TABLE `relationship_interface_operation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relationship_interface_operation_input_output`
--

DROP TABLE IF EXISTS `relationship_interface_operation_input_output`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relationship_interface_operation_input_output` (
  `id` char(36) NOT NULL,
  `name` char(255) NOT NULL,
  `value_storage_id` char(36) NOT NULL,
  `operation_id` char(36) NOT NULL,
  `type` enum('input','output') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_interface_operation_input_output_operation_fk` (`operation_id`),
  KEY `relationship_interface_operation_input_output_value_storage_fk` (`value_storage_id`),
  CONSTRAINT `relationship_interface_operation_input_output_operation_fk` FOREIGN KEY (`operation_id`) REFERENCES `relationship_interface_operation` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relationship_interface_operation_input_output_value_storage_fk` FOREIGN KEY (`value_storage_id`) REFERENCES `value_storage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationship_interface_operation_input_output`
--

LOCK TABLES `relationship_interface_operation_input_output` WRITE;
/*!40000 ALTER TABLE `relationship_interface_operation_input_output` DISABLE KEYS */;
/*!40000 ALTER TABLE `relationship_interface_operation_input_output` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requirement`
--

DROP TABLE IF EXISTS `requirement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `requirement` (
  `id` char(36) NOT NULL,
  `capability` char(255) DEFAULT NULL,
  `name` char(255) NOT NULL,
  `node_id` char(36) NOT NULL,
  `node` char(255) DEFAULT NULL,
  `node_link` char(36) DEFAULT NULL,
  `relationship_type` char(255) NOT NULL,
  `order` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `requirement_node_template_id_fk_2` (`node_link`),
  KEY `requirement_node_template_null_fk` (`node_id`),
  CONSTRAINT `requirement_node_template_id_fk_2` FOREIGN KEY (`node_link`) REFERENCES `node_template` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `requirement_node_template_null_fk` FOREIGN KEY (`node_id`) REFERENCES `node_template` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requirement`
--

LOCK TABLES `requirement` WRITE;
/*!40000 ALTER TABLE `requirement` DISABLE KEYS */;
/*!40000 ALTER TABLE `requirement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ts_to_as`
--

DROP TABLE IF EXISTS `ts_to_as`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ts_to_as` (
  `artifact_storage_id` char(36) NOT NULL,
  `type_storage_id` char(36) NOT NULL,
  PRIMARY KEY (`artifact_storage_id`,`type_storage_id`),
  KEY `ts_to_as_type_null_fk` (`type_storage_id`),
  CONSTRAINT `foreign_key_name` FOREIGN KEY (`artifact_storage_id`) REFERENCES `artifact_storage` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ts_to_as_type_null_fk` FOREIGN KEY (`type_storage_id`) REFERENCES `type` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ts_to_as`
--

LOCK TABLES `ts_to_as` WRITE;
/*!40000 ALTER TABLE `ts_to_as` DISABLE KEYS */;
/*!40000 ALTER TABLE `ts_to_as` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type`
--

DROP TABLE IF EXISTS `type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `type` (
  `id` char(36) NOT NULL,
  `version` char(32) DEFAULT NULL,
  `type_of_type` enum('artifact_type','data_type','capability_type','interface_type','relationship_type','node_type','group_type','policy_type') NOT NULL,
  `type_name` char(64) NOT NULL,
  `data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `header_id` char(36) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `type_type_header_null_fk` (`header_id`),
  CONSTRAINT `type_type_header_null_fk` FOREIGN KEY (`header_id`) REFERENCES `type_header` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `data` CHECK (json_valid(`data`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type`
--

LOCK TABLES `type` WRITE;
/*!40000 ALTER TABLE `type` DISABLE KEYS */;
INSERT INTO `type` VALUES
('000376f3-df10-49b1-91e7-a1eca47dfd4b','1.0','capability_type','tosca.capabilities.Scalable','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Root\\\", \\\"description\\\": \\\"This is the default TOSCA type that should be used to express a scalability capability for a node.\\\", \\\"properties\\\": {\\\"min_instances\\\": {\\\"type\\\": \\\"integer\\\", \\\"description\\\": \\\"This property is used to indicate the minimum number of instances that should be created for the associated TOSCA Node Template by a TOSCA orchestrator.\\\\n\\\", \\\"default\\\": 1}, \\\"max_instances\\\": {\\\"type\\\": \\\"integer\\\", \\\"description\\\": \\\"This property is used to indicate the maximum number of instances that should be created for the associated TOSCA Node Template by a TOSCA orchestrator.\\\\n\\\", \\\"default\\\": 1}, \\\"default_instances\\\": {\\\"type\\\": \\\"integer\\\", \\\"description\\\": \\\"An optional property that indicates the requested default number of instances that should be the starting number of instances a TOSCA orchestrator should attempt to allocate. Note: The value for this property MUST be in the range between the values set for \\\\u2018min_instances\\\\u2019 and \\\\u2018max_instances\\\\u2019 properties.\\\\n\\\", \\\"required\\\": false, \\\"default\\\": 1}}}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('01e52fba-0d13-4649-9932-90dcb7670a34','1.0','data_type','scalar-unit.size','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"scalar-unit.size\\\", \\\"specification.citation\\\": \\\"[TOSCA-Simple-Profile-YAML-v1.3]\\\", \\\"specification.location\\\": \\\"3.3.6.4\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('021a9188-0f8f-4c1e-bc5c-6d928aa63e28','1.0','data_type','tosca.datatypes.network.PortDef','\"{\\\"derived_from\\\": \\\"integer\\\", \\\"description\\\": \\\"The PortDef type defines a network port.\\\", \\\"constraints\\\": [{\\\"in_range\\\": [1, 65535]}]}\"','24064643-f88b-4f8d-9c15-beaf43e04728'),
('09290690-5cc9-4fe7-af72-5c4e5909b1e8','1.0','capability_type','tosca.capabilities.Network','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Root\\\", \\\"description\\\": \\\"The Network capability, when included on a Node Type or Template definition, indicates that the node can provide addressiblity for the resource on a named network with the specified ports.\\\", \\\"properties\\\": {\\\"name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The otional name (or identifier) of a specific network resource.\\\", \\\"required\\\": false}}}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('0b202160-8ffb-4997-97b7-1716553e140d','1.0','data_type','boolean','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"ard.boolean\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('1407a492-2142-40f4-898b-b03b2b29717e','1.0','capability_type','tosca.capabilities.Endpoint.Public','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Endpoint\\\", \\\"description\\\": \\\"This capability represents a public endpoint which is accessible to the general internet (and its public IP address ranges). This public endpoint capability also can be used to create a floating (IP) address that the underlying network assigns from a pool allocated from the application\\\\u2019s underlying public network. This floating address is managed by the underlying network such that can be routed an application\\\\u2019s private address and remains reliable to internet clients.\\\\n\\\", \\\"properties\\\": {\\\"network_name\\\": {\\\"type\\\": \\\"string\\\", \\\"default\\\": \\\"PUBLIC\\\", \\\"constraints\\\": [{\\\"equal\\\": \\\"PUBLIC\\\"}]}, \\\"floating\\\": {\\\"type\\\": \\\"boolean\\\", \\\"description\\\": \\\"Indicates that the public address should be allocated from a pool of floating IPs that are associated with the network.\\\\n\\\", \\\"default\\\": false}, \\\"dns_name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The optional name to register with DNS\\\", \\\"required\\\": false}}}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('14906a21-00c1-4138-8819-010407ddee23','1.0','node_type','tosca.nodes.WebApplication','\"{\\\"derived_from\\\": \\\"tosca.nodes.Root\\\", \\\"description\\\": \\\"The TOSCA WebApplication node represents a software application that can be managed and run by a TOSCA WebServer node.  Specific types of web applications such as Java, etc. could be derived from this type.\\\\n\\\", \\\"properties\\\": {\\\"context_root\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The web application\\\\u2019s context root which designates the application\\\\u2019s URL path within the web server it is hosted on.\\\", \\\"required\\\": false}}, \\\"requirements\\\": [{\\\"host\\\": {\\\"capability\\\": \\\"tosca.capabilities.Compute\\\", \\\"node\\\": \\\"tosca.nodes.WebServer\\\", \\\"relationship\\\": \\\"tosca.relationships.HostedOn\\\"}}], \\\"capabilities\\\": {\\\"app_endpoint\\\": {\\\"type\\\": \\\"tosca.capabilities.Endpoint\\\"}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('167068c0-77d8-4a29-a4f3-6690f74ef646','1.0','data_type','tosca.datatypes.Credential','\"{\\\"derived_from\\\": \\\"tosca.datatypes.Root\\\", \\\"description\\\": \\\"The Credential type is a complex TOSCA data Type used when describing authorization credentials used to access network accessible resources.\\\", \\\"properties\\\": {\\\"protocol\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The optional protocol name.\\\", \\\"required\\\": false}, \\\"token_type\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The required token type.\\\", \\\"default\\\": \\\"password\\\"}, \\\"token\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The required token used as a credential for authorization or access to a networked resource.\\\"}, \\\"keys\\\": {\\\"type\\\": \\\"map\\\", \\\"description\\\": \\\"The optional list of protocol-specific keys or assertions.\\\", \\\"required\\\": false, \\\"entry_schema\\\": {\\\"type\\\": \\\"string\\\"}}, \\\"user\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The optional user (name or ID) used for non-token based credentials.\\\", \\\"required\\\": false}}}\"','24064643-f88b-4f8d-9c15-beaf43e04728'),
('1a8d85c6-c730-412d-bb22-2a3b732101fd','1.0','capability_type','tosca.capabilities.Container','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Root\\\", \\\"description\\\": \\\"The Container capability, when included on a Node Type or Template definition, indicates that the node can act as a container for (or a host for) one or more other declared Node Types.\\\"}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('21f1991c-bd10-4bc9-acad-83a78eff0b40','1.0','node_type','tosca.nodes.Abstract.Compute','\"{\\\"derived_from\\\": \\\"tosca.nodes.Root\\\", \\\"description\\\": \\\"The TOSCA Abstract.Compute node represents an abstract compute resource without any requirements on storage or network resources.\\\", \\\"capabilities\\\": {\\\"host\\\": {\\\"type\\\": \\\"tosca.capabilities.Compute\\\"}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('24261fc6-ba8a-4aac-9478-01b214e656f2','1.0','relationship_type','tosca.relationships.AttachesTo','\"{\\\"derived_from\\\": \\\"tosca.relationships.Root\\\", \\\"properties\\\": {\\\"location\\\": {\\\"type\\\": \\\"string\\\", \\\"constraints\\\": [{\\\"min_length\\\": 1}]}, \\\"device\\\": {\\\"type\\\": \\\"string\\\", \\\"required\\\": false}}, \\\"valid_target_types\\\": [\\\"tosca.capabilities.Attachment\\\"]}\"','ef3f4a83-6736-495d-921d-e5359edf82ab'),
('287e9666-5a5e-402a-9458-6fda8b89ea28','1.0','node_type','tosca.nodes.Container.Application','\"{\\\"derived_from\\\": \\\"tosca.nodes.Root\\\", \\\"description\\\": \\\"The TOSCA Container Application node represents an application that requires Container-level virtualization technology.\\\\n\\\", \\\"requirements\\\": [{\\\"host\\\": {\\\"capability\\\": \\\"tosca.capabilities.Compute\\\", \\\"node\\\": \\\"tosca.nodes.Container.Runtime\\\", \\\"relationship\\\": \\\"tosca.relationships.HostedOn\\\"}}, {\\\"storage\\\": {\\\"capability\\\": \\\"tosca.capabilities.Storage\\\"}}, {\\\"network\\\": {\\\"capability\\\": \\\"tosca.capabilities.Endpoint\\\"}}]}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('2a89a450-cca9-4764-973f-82988d43618e','1.0','data_type','list','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"ard.list\\\", \\\"specification.citation\\\": \\\"[TOSCA-Simple-Profile-YAML-v1.3]\\\", \\\"specification.location\\\": \\\"3.3.4\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('2e00eacc-9e0a-4175-a70f-190cd16ef922','1.0','node_type','tosca.nodes.Abstract.Storage','\"{\\\"derived_from\\\": \\\"tosca.nodes.Root\\\", \\\"description\\\": \\\"The TOSCA Abstract.Storage node represents an abstract storage resource without any requirements on compute or network resources.\\\", \\\"properties\\\": {\\\"name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The logical name (or ID) of the storage resource.\\\"}, \\\"size\\\": {\\\"type\\\": \\\"scalar-unit.size\\\", \\\"description\\\": \\\"The requested initial storage size (default unit is in Gigabytes).\\\", \\\"default\\\": \\\"0 MB\\\", \\\"constraints\\\": [{\\\"greater_or_equal\\\": \\\"0 MB\\\"}]}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('3040aa3f-01fc-48f6-b635-1660b73533e0','1.0','data_type','tosca.datatypes.xml','\"{\\\"derived_from\\\": \\\"string\\\", \\\"description\\\": \\\"The xml type defines a string that containst data in the Extensible Markup Language (XML) format.\\\"}\"','24064643-f88b-4f8d-9c15-beaf43e04728'),
('352fee6f-2d4b-424c-8ff2-38f19b2a2273','1.0','data_type','version','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"version\\\", \\\"puccini.comparer\\\": \\\"tosca.comparer.version\\\", \\\"specification.citation\\\": \\\"[TOSCA-Simple-Profile-YAML-v1.3]\\\", \\\"specification.location\\\": \\\"3.3.2\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('3930f20a-f86a-4d27-85cc-bdc722567c4f','1.0','relationship_type','tosca.relationships.network.LinksTo','\"{\\\"derived_from\\\": \\\"tosca.relationships.DependsOn\\\", \\\"description\\\": \\\"This relationship type represents an association relationship between Port and Network node types.\\\\n\\\", \\\"valid_target_types\\\": [\\\"tosca.capabilities.network.Linkable\\\"]}\"','ef3f4a83-6736-495d-921d-e5359edf82ab'),
('3d8ad2c1-9402-4ca0-86cc-f39c35ed5030','1.0','node_type','tosca.nodes.Database','\"{\\\"derived_from\\\": \\\"tosca.nodes.Root\\\", \\\"description\\\": \\\"The TOSCA Database node represents a logical database that can be managed and hosted by a TOSCA DBMS node.\\\", \\\"properties\\\": {\\\"name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"the logical name of the database\\\", \\\"required\\\": true}, \\\"port\\\": {\\\"type\\\": \\\"integer\\\", \\\"description\\\": \\\"the port the underlying database service will listen to for data\\\", \\\"required\\\": false}, \\\"user\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"the optional user account name for DB administration\\\", \\\"required\\\": false}, \\\"password\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"the optional password for the DB user account\\\", \\\"required\\\": false}}, \\\"requirements\\\": [{\\\"host\\\": {\\\"capability\\\": \\\"tosca.capabilities.Compute\\\", \\\"node\\\": \\\"tosca.nodes.DBMS\\\", \\\"relationship\\\": \\\"tosca.relationships.HostedOn\\\"}}], \\\"capabilities\\\": {\\\"database_endpoint\\\": {\\\"type\\\": \\\"tosca.capabilities.Endpoint.Database\\\"}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('47523d15-fa4d-4081-b066-784d139654a4','1.0','node_type','tosca.nodes.Storage.ObjectStorage','\"{\\\"derived_from\\\": \\\"tosca.nodes.Abstract.Storage\\\", \\\"description\\\": \\\"The TOSCA ObjectStorage node represents storage that provides the ability to store data as objects (or BLOBs of data) without consideration for the underlying filesystem or devices.\\\", \\\"properties\\\": {\\\"maxsize\\\": {\\\"type\\\": \\\"scalar-unit.size\\\", \\\"description\\\": \\\"The requested maximum storage size (default unit is in Gigabytes).\\\", \\\"required\\\": false, \\\"constraints\\\": [{\\\"greater_or_equal\\\": \\\"0 GB\\\"}]}}, \\\"capabilities\\\": {\\\"storage_endpoint\\\": {\\\"type\\\": \\\"tosca.capabilities.Endpoint\\\"}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('4bd0248a-a4eb-4273-95dd-78fd78a3e24e','1.0','data_type','tosca.datatypes.Root','\"{\\\"description\\\": \\\"The TOSCA root Data Type all other TOSCA base Data Types derive from.\\\"}\"','24064643-f88b-4f8d-9c15-beaf43e04728'),
('53f750ec-fd52-4356-a744-8bbdabc5bd1a','1.0','node_type','tosca.nodes.Compute','\"{\\\"derived_from\\\": \\\"tosca.nodes.Abstract.Compute\\\", \\\"description\\\": \\\"The TOSCA Compute node represents one or more real or virtual processors of software applications or services along with other essential local resources.  Collectively, the resources the compute node represents can logically be viewed as a (real or virtual) \\\\u201cserver\\\\u201d.\\\\n\\\", \\\"attributes\\\": {\\\"private_address\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The primary private IP address assigned by the cloud provider that applications may use to access the Compute node.\\\"}, \\\"public_address\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The primary public IP address assigned by the cloud provider that applications may use to access the Compute node.\\\"}, \\\"networks\\\": {\\\"type\\\": \\\"map\\\", \\\"entry_schema\\\": {\\\"type\\\": \\\"tosca.datatypes.network.NetworkInfo\\\"}}, \\\"ports\\\": {\\\"type\\\": \\\"map\\\", \\\"entry_schema\\\": {\\\"type\\\": \\\"tosca.datatypes.network.PortInfo\\\"}}}, \\\"requirements\\\": [{\\\"local_storage\\\": {\\\"capability\\\": \\\"tosca.capabilities.Attachment\\\", \\\"node\\\": \\\"tosca.nodes.Storage.BlockStorage\\\", \\\"relationship\\\": \\\"tosca.relationships.AttachesTo\\\", \\\"occurrences\\\": [0, \\\"UNBOUNDED\\\"]}}], \\\"capabilities\\\": {\\\"host\\\": {\\\"type\\\": \\\"tosca.capabilities.Compute\\\", \\\"valid_source_types\\\": [\\\"tosca.nodes.SoftwareComponent\\\"]}, \\\"os\\\": {\\\"type\\\": \\\"tosca.capabilities.OperatingSystem\\\"}, \\\"endpoint\\\": {\\\"type\\\": \\\"tosca.capabilities.Endpoint.Admin\\\"}, \\\"scalable\\\": {\\\"type\\\": \\\"tosca.capabilities.Scalable\\\"}, \\\"binding\\\": {\\\"type\\\": \\\"tosca.capabilities.network.Bindable\\\"}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('57ae1f2a-60af-4e5e-af17-cb0ddef450fb','1.0','data_type','scalar-unit.time','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"scalar-unit.time\\\", \\\"specification.citation\\\": \\\"[TOSCA-Simple-Profile-YAML-v1.3]\\\", \\\"specification.location\\\": \\\"3.3.6.5\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('5bdae233-4d12-4c1a-917c-1ec9ec8474ff','1.0','node_type','tosca.nodes.Storage.BlockStorage','\"{\\\"derived_from\\\": \\\"tosca.nodes.Abstract.Storage\\\", \\\"description\\\": \\\"The TOSCA BlockStorage node currently represents a server-local block storage device (i.e., not shared) offering evenly sized blocks of data from which raw storage volumes can be created.\\\\n\\\", \\\"properties\\\": {\\\"size\\\": {\\\"type\\\": \\\"scalar-unit.size\\\", \\\"default\\\": \\\"1 MB\\\", \\\"constraints\\\": [{\\\"greater_or_equal\\\": \\\"1 MB\\\"}]}, \\\"volume_id\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"ID of an existing volume (that is in the accessible scope of the requesting application).\\\", \\\"required\\\": false}, \\\"snapshot_id\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"Some identifier that represents an existing snapshot that should be used when creating the block storage (volume).\\\", \\\"required\\\": false}}, \\\"capabilities\\\": {\\\"attachment\\\": {\\\"type\\\": \\\"tosca.capabilities.Attachment\\\"}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('5e2082d8-f47f-4e40-9a60-b536627cf382','1.0','data_type','tosca.datatypes.network.PortInfo','\"{\\\"derived_from\\\": \\\"tosca.datatypes.Root\\\", \\\"description\\\": \\\"The PortInfo type describes network port information.\\\", \\\"properties\\\": {\\\"port_name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The logical network port name.\\\"}, \\\"port_id\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The unique ID for the network port generated by the network provider.\\\"}, \\\"network_id\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The unique ID for the network.\\\"}, \\\"mac_address\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The unique media access control address (MAC address) assigned to the port.\\\"}, \\\"addresses\\\": {\\\"type\\\": \\\"list\\\", \\\"description\\\": \\\"The list of IP address(es) assigned to the port.\\\", \\\"entry_schema\\\": {\\\"type\\\": \\\"string\\\"}}}}\"','24064643-f88b-4f8d-9c15-beaf43e04728'),
('5e4154bb-00e1-4709-b96e-1b2bfb2ccd3e','1.0','capability_type','tosca.capabilities.Endpoint.Database','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Endpoint\\\", \\\"description\\\": \\\"This is the default TOSCA type that should be used or extended to define a specialized database endpoint capability.\\\"}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('5fd21b61-4ec3-43eb-a5d1-85d120f2a969','1.0','node_type','tosca.nodes.LoadBalancer','\"{\\\"derived_from\\\": \\\"tosca.nodes.Root\\\", \\\"description\\\": \\\"The TOSCA Load Balancer node represents logical function that be used in conjunction with a Floating Address to distribute an application\\\\u2019s traffic (load) across a number of instances of the application (e.g., for a clustered or scaled application).\\\\n\\\", \\\"properties\\\": {\\\"algorithm\\\": {\\\"type\\\": \\\"string\\\", \\\"required\\\": false}}, \\\"requirements\\\": [{\\\"application\\\": {\\\"capability\\\": \\\"tosca.capabilities.Endpoint\\\", \\\"relationship\\\": \\\"tosca.relationships.RoutesTo\\\", \\\"occurrences\\\": [0, \\\"UNBOUNDED\\\"]}}], \\\"capabilities\\\": {\\\"client\\\": {\\\"type\\\": \\\"tosca.capabilities.Endpoint.Public\\\", \\\"description\\\": \\\"the Floating (IP) client\\\\u2019s on the public network can connect to\\\", \\\"occurrences\\\": [0, \\\"UNBOUNDED\\\"]}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('63952774-b91f-4707-bf7e-38dd899fcd1a','1.0','node_type','tosca.nodes.WebServer','\"{\\\"derived_from\\\": \\\"tosca.nodes.SoftwareComponent\\\", \\\"description\\\": \\\"This TOSCA WebServer Node Type represents an abstract software component or service that is capable of hosting and providing management operations for one or more WebApplication nodes.\\\\n\\\", \\\"capabilities\\\": {\\\"data_endpoint\\\": \\\"tosca.capabilities.Endpoint\\\", \\\"admin_endpoint\\\": \\\"tosca.capabilities.Endpoint.Admin\\\", \\\"host\\\": {\\\"type\\\": \\\"tosca.capabilities.Compute\\\", \\\"valid_source_types\\\": [\\\"tosca.nodes.WebApplication\\\"]}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('6472f3d0-0686-466e-9884-8d722c95d4b4','1.0','capability_type','tosca.capabilities.Root','\"{\\\"description\\\": \\\"This is the default (root) TOSCA Capability Type definition that all other TOSCA Capability Types derive from.\\\"}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('67666f4e-cccd-46be-ad2b-d644735cb2e1','1.0','data_type','float','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"ard.float\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('69b3024b-e701-4851-841a-fe57a7563924','1.0','interface_type','tosca.interfaces.relationship.Configure','\"{\\\"derived_from\\\": \\\"tosca.interfaces.Root\\\", \\\"operations\\\": {\\\"pre_configure_source\\\": {\\\"description\\\": \\\"Operation to pre-configure the source endpoint.\\\"}, \\\"pre_configure_target\\\": {\\\"description\\\": \\\"Operation to pre-configure the target endpoint.\\\"}, \\\"post_configure_source\\\": {\\\"description\\\": \\\"Operation to post-configure the source endpoint.\\\"}, \\\"post_configure_target\\\": {\\\"description\\\": \\\"Operation to post-configure the target endpoint.\\\"}, \\\"add_target\\\": {\\\"description\\\": \\\"Operation to notify the source node of a target node being added via a relationship.\\\"}, \\\"add_source\\\": {\\\"description\\\": \\\"Operation to notify the target node of a source node which is now available via a relationship.\\\"}, \\\"target_changed\\\": {\\\"description\\\": \\\"Operation to notify source some property or attribute of the target changed\\\"}, \\\"remove_target\\\": {\\\"description\\\": \\\"Operation to remove a target node.\\\"}}}\"','a35fbf65-ca8d-4f88-b0bf-6930f2e51cdd'),
('6c5a582b-bd1f-43ac-b2a9-01a7b8e30814','1.0','artifact_type','tosca.artifacts.Deployment.Image','\"{\\\"derived_from\\\": \\\"tosca.artifacts.Deployment\\\", \\\"description\\\": \\\"This artifact type represents a parent type for any \\\\u201cimage\\\\u201d which is an opaque packaging of a TOSCA Node\\\\u2019s deployment (whether real or virtual) whose contents are typically already installed and pre-configured (i.e., \\\\u201cstateful\\\\u201d) and prepared to be run on a known target container.\\\\n\\\"}\"','32e6275f-8d7b-4449-b0f9-36d4d42e3833'),
('6d1058b9-cd35-4fef-a228-7e9c2ae5e70a','1.0','capability_type','tosca.capabilities.OperatingSystem','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Root\\\", \\\"description\\\": \\\"This is the default TOSCA type that should be used to express an Operating System capability for a node.\\\", \\\"properties\\\": {\\\"architecture\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The Operating System (OS) architecture.  Examples of valid values include: x86_32, x86_64, etc.\\\\n\\\", \\\"required\\\": false}, \\\"type\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The Operating System (OS) type.  Examples of valid values include: linux, aix, mac, windows, etc.\\\\n\\\", \\\"required\\\": false}, \\\"distribution\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The Operating System (OS) distribution.  Examples of valid values for an \\\\u201ctype\\\\u201d of \\\\u201cLinux\\\\u201d would include: debian, fedora, rhel and ubuntu.\\\\n\\\", \\\"required\\\": false}, \\\"version\\\": {\\\"type\\\": \\\"version\\\", \\\"description\\\": \\\"The Operating System version.\\\\n\\\", \\\"required\\\": false}}}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('70b9af4f-e19f-4872-9cf2-e159c77fdb1d','1.0','interface_type','tosca.interfaces.node.lifecycle.Standard','\"{\\\"derived_from\\\": \\\"tosca.interfaces.Root\\\", \\\"operations\\\": {\\\"create\\\": {\\\"description\\\": \\\"Standard lifecycle create operation.\\\"}, \\\"configure\\\": {\\\"description\\\": \\\"Standard lifecycle configure operation.\\\"}, \\\"start\\\": {\\\"description\\\": \\\"Standard lifecycle start operation.\\\"}, \\\"stop\\\": {\\\"description\\\": \\\"Standard lifecycle stop operation.\\\"}, \\\"delete\\\": {\\\"description\\\": \\\"Standard lifecycle delete operation.\\\"}}}\"','a35fbf65-ca8d-4f88-b0bf-6930f2e51cdd'),
('7d2d7343-ee04-461c-a400-5e0687cdfd05','1.0','data_type','integer','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"ard.integer\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('7e4d568c-55dc-46f2-be18-24c6c77066e3','1.0','relationship_type','tosca.relationships.Root','\"{\\\"description\\\": \\\"The TOSCA root Relationship Type all other TOSCA base Relationship Types derive from\\\", \\\"attributes\\\": {\\\"tosca_id\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"A unique identifier of the realized instance of a Relationship Template that derives from any TOSCA normative type.\\\"}, \\\"tosca_name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"This attribute reflects the name of the Relationship Template as defined in the TOSCA service template.  This name is not unique to the realized instance model of corresponding deployed application as each template in the model can result in one or more instances (e.g., scaled) when orchestrated to a provider environment.\\\\n\\\"}, \\\"state\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The state of the relationship instance.\\\", \\\"default\\\": \\\"initial\\\"}}, \\\"interfaces\\\": {\\\"Configure\\\": {\\\"type\\\": \\\"tosca.interfaces.relationship.Configure\\\"}}}\"','ef3f4a83-6736-495d-921d-e5359edf82ab'),
('7ff254c8-9ff2-4ad5-bba6-7f8044c2d9ab','1.0','node_type','tosca.nodes.Container.Runtime','\"{\\\"derived_from\\\": \\\"tosca.nodes.SoftwareComponent\\\", \\\"description\\\": \\\"The TOSCA Container Runtime node represents operating system-level virtualization technology used to run multiple application services on a single Compute host.\\\\n\\\", \\\"capabilities\\\": {\\\"host\\\": {\\\"type\\\": \\\"tosca.capabilities.Compute\\\", \\\"valid_source_types\\\": [\\\"tosca.nodes.Container.Application\\\"]}, \\\"scalable\\\": {\\\"type\\\": \\\"tosca.capabilities.Scalable\\\"}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('86e5c335-519f-4319-af3f-d82566dc5880','1.0','capability_type','tosca.capabilities.network.Linkable','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Node\\\", \\\"description\\\": \\\"A node type that includes the Linkable capability indicates that it can be pointed to by a tosca.relationships.network.LinksTo relationship type.\\\"}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('8f1aa978-9541-4c40-95da-182b774d4759','1.0','data_type','tosca.datatypes.json','\"{\\\"derived_from\\\": \\\"string\\\", \\\"description\\\": \\\"The json type defines a string that containst data in the JavaScript Object Notation (JSON) format.\\\"}\"','24064643-f88b-4f8d-9c15-beaf43e04728'),
('904f2ead-4fd4-49f9-b719-382124dd19fd','1.0','capability_type','tosca.capabilities.Compute','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Container\\\", \\\"description\\\": \\\"The Compute capability, when included on a Node Type or Template definition, indicates that the node can provide hosting on a named compute resource.\\\\n\\\", \\\"properties\\\": {\\\"name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The otional name (or identifier) of a specific compute resource for hosting.\\\", \\\"required\\\": false}, \\\"num_cpus\\\": {\\\"type\\\": \\\"integer\\\", \\\"description\\\": \\\"Number of (actual or virtual) CPUs associated with the Compute node.\\\", \\\"required\\\": false, \\\"constraints\\\": [{\\\"greater_or_equal\\\": 1}]}, \\\"cpu_frequency\\\": {\\\"type\\\": \\\"scalar-unit.frequency\\\", \\\"description\\\": \\\"Specifies the operating frequency of CPU\'s core.  This property expresses the expected frequency of one (1) CPU as provided by the property \\\\u201cnum_cpus\\\\u201d.\\\\n\\\", \\\"required\\\": false, \\\"constraints\\\": [{\\\"greater_or_equal\\\": \\\"0.1 GHz\\\"}]}, \\\"disk_size\\\": {\\\"type\\\": \\\"scalar-unit.size\\\", \\\"description\\\": \\\"Size of the local disk available to applications running on the Compute node (default unit is MB).\\\", \\\"required\\\": false, \\\"constraints\\\": [{\\\"greater_or_equal\\\": \\\"0 MB\\\"}]}, \\\"mem_size\\\": {\\\"type\\\": \\\"scalar-unit.size\\\", \\\"description\\\": \\\"Size of memory available to applications running on the Compute node (default unit is MB).\\\", \\\"required\\\": false, \\\"constraints\\\": [{\\\"greater_or_equal\\\": \\\"0 MB\\\"}]}}}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('91d73b84-83b0-43ff-99d6-ea51611a5418','1.0','capability_type','tosca.capabilities.Endpoint','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Root\\\", \\\"description\\\": \\\"This is the default TOSCA type that should be used or extended to define a network endpoint capability.  This includes the information to express a basic endpoint with a single port or a complex endpoint with multiple ports.  By default the Endpoint is assumed to represent an address on a private network unless otherwise specified.\\\\n\\\", \\\"properties\\\": {\\\"protocol\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The name of the protocol (i.e., the protocol prefix) that the endpoint accepts (any OSI Layer 4-7 protocols) Examples: http, https, ftp, tcp, udp, etc.\\\\n\\\", \\\"default\\\": \\\"tcp\\\"}, \\\"port\\\": {\\\"type\\\": \\\"tosca.datatypes.network.PortDef\\\", \\\"description\\\": \\\"The optional port of the endpoint.\\\", \\\"required\\\": false}, \\\"secure\\\": {\\\"type\\\": \\\"boolean\\\", \\\"description\\\": \\\"Requests for the endpoint to be secure and use credentials supplied on the ConnectsTo relationship.\\\", \\\"required\\\": false, \\\"default\\\": false}, \\\"url_path\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The optional URL path of the endpoint\\\\u2019s address if applicable for the protocol.\\\", \\\"required\\\": false}, \\\"port_name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The optional name (or ID) of the network port this endpoint should be bound to.\\\", \\\"required\\\": false}, \\\"network_name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The optional name (or ID) of the network this endpoint should be bound to.  network_name: PRIVATE | PUBLIC |<network_name> | <network_id>\\\\n\\\", \\\"required\\\": false, \\\"default\\\": \\\"PRIVATE\\\"}, \\\"initiator\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The optional indicator of the direction of the connection.\\\", \\\"required\\\": false, \\\"default\\\": \\\"source\\\", \\\"constraints\\\": [{\\\"valid_values\\\": [\\\"source\\\", \\\"target\\\", \\\"peer\\\"]}]}, \\\"ports\\\": {\\\"type\\\": \\\"map\\\", \\\"description\\\": \\\"The optional map of ports the Endpoint supports (if more than one).\\\", \\\"required\\\": false, \\\"constraints\\\": [{\\\"min_length\\\": 1}], \\\"entry_schema\\\": {\\\"type\\\": \\\"tosca.datatypes.network.PortSpec\\\"}}}, \\\"attributes\\\": {\\\"ip_address\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"This is the IP address as propagated up by the associated node\\\\u2019s host (Compute) container.\\\"}}}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('9980c7b8-9d61-4d1c-b8a1-e85af5a68d63','1.0','capability_type','tosca.capabilities.Attachment','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Root\\\", \\\"description\\\": \\\"This is the default TOSCA type that should be used or extended to define an attachment capability of a (logical) infrastructure device node (e.g., BlockStorage node).\\\\n\\\"}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('9b5d61a4-5f0d-4999-ac20-fbfb09efcba5','1.0','relationship_type','tosca.relationships.ConnectsTo','\"{\\\"derived_from\\\": \\\"tosca.relationships.Root\\\", \\\"description\\\": \\\"This type represents a network connection relationship between two nodes.\\\", \\\"properties\\\": {\\\"credential\\\": {\\\"type\\\": \\\"tosca.datatypes.Credential\\\", \\\"description\\\": \\\"The security credential to use to present to the target endpoint to for either authentication or authorization purposes.\\\", \\\"required\\\": false}}, \\\"valid_target_types\\\": [\\\"tosca.capabilities.Endpoint\\\"]}\"','ef3f4a83-6736-495d-921d-e5359edf82ab'),
('a04503ba-e6ed-4412-9f89-c1464db9c877','1.0','artifact_type','tosca.artifacts.Implementation.Bash','\"{\\\"derived_from\\\": \\\"tosca.artifacts.Implementation\\\", \\\"description\\\": \\\"Script artifact for the Unix Bash shell\\\", \\\"mime_type\\\": \\\"application/x-sh\\\", \\\"file_ext\\\": [\\\"sh\\\"]}\"','32e6275f-8d7b-4449-b0f9-36d4d42e3833'),
('a317c160-3943-49d0-ae33-7051d8c3fb40','1.0','data_type','range','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"range\\\", \\\"specification.citation\\\": \\\"[TOSCA-Simple-Profile-YAML-v1.3]\\\", \\\"specification.location\\\": \\\"3.3.3\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('a74c3b1c-ee6f-4451-9512-a7e06d9ba144','1.0','data_type','timestamp','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"timestamp\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('aa0ebe0d-14c8-4d21-b064-813e4c4f9f90','1.0','node_type','tosca.nodes.SoftwareComponent','\"{\\\"derived_from\\\": \\\"tosca.nodes.Root\\\", \\\"description\\\": \\\"The TOSCA SoftwareComponent node represents a generic software component that can be managed and run by a TOSCA Compute Node Type.\\\", \\\"properties\\\": {\\\"component_version\\\": {\\\"type\\\": \\\"version\\\", \\\"description\\\": \\\"The optional software component\\\\u2019s version.\\\", \\\"required\\\": false}, \\\"admin_credential\\\": {\\\"type\\\": \\\"tosca.datatypes.Credential\\\", \\\"description\\\": \\\"The optional credential that can be used to authenticate to the software component.\\\", \\\"required\\\": false}}, \\\"requirements\\\": [{\\\"host\\\": {\\\"capability\\\": \\\"tosca.capabilities.Compute\\\", \\\"node\\\": \\\"tosca.nodes.Compute\\\", \\\"relationship\\\": \\\"tosca.relationships.HostedOn\\\"}}]}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('b1bf0e6e-e221-4c5d-8f3b-36b68a41bd73','1.0','interface_type','tosca.interfaces.Root','\"{\\\"description\\\": \\\"The TOSCA root Interface Type all other TOSCA base Interface Types derive from.\\\"}\"','a35fbf65-ca8d-4f88-b0bf-6930f2e51cdd'),
('b3c331cc-dcac-4441-8714-4d338ab96913','1.0','artifact_type','tosca.artifacts.Deployment.Image.VM','\"{\\\"derived_from\\\": \\\"tosca.artifacts.Deployment.Image\\\", \\\"description\\\": \\\"This artifact represents the parent type for all Virtual Machine (VM) image and container formatted deployment artifacts.  These images contain a stateful capture of a machine (e.g., server) including operating system and installed software along with any configurations and can be run on another machine using a hypervisor which virtualizes typical server (i.e., hardware) resources.  Virtual Machine (VM) Image\\\\n\\\"}\"','32e6275f-8d7b-4449-b0f9-36d4d42e3833'),
('b4da3aab-9f39-49e0-9bb3-5e16dbb92c78','1.0','data_type','tosca.datatypes.TimeInterval','\"{\\\"derived_from\\\": \\\"tosca.datatypes.Root\\\", \\\"description\\\": \\\"The TimeInterval type describes a period of time using the YAML ISO 8601 format to declare the start and end times.\\\", \\\"properties\\\": {\\\"start_time\\\": {\\\"type\\\": \\\"timestamp\\\", \\\"description\\\": \\\"The inclusive start time for the time interval.\\\", \\\"required\\\": true}, \\\"end_time\\\": {\\\"type\\\": \\\"timestamp\\\", \\\"description\\\": \\\"The inclusive end time for the time interval.\\\", \\\"required\\\": true}}}\"','24064643-f88b-4f8d-9c15-beaf43e04728'),
('b5f61792-734e-4886-81ad-d22d9e345b76','1.0','data_type','scalar-unit.frequency','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"scalar-unit.frequency\\\", \\\"specification.citation\\\": \\\"[TOSCA-Simple-Profile-YAML-v1.3]\\\", \\\"specification.location\\\": \\\"3.3.6.6\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('ba1f561a-81b6-418d-a0ff-8b3c4c265aba','1.0','artifact_type','tosca.artifacts.Deployment','\"{\\\"derived_from\\\": \\\"tosca.artifacts.Root\\\", \\\"description\\\": \\\"TOSCA base type for deployment artifacts\\\"}\"','32e6275f-8d7b-4449-b0f9-36d4d42e3833'),
('be20ab7c-a549-426f-af1a-2a0d90e1b5dd','1.0','relationship_type','tosca.relationships.HostedOn','\"{\\\"derived_from\\\": \\\"tosca.relationships.Root\\\", \\\"description\\\": \\\"This type represents a hosting relationship between two nodes.\\\", \\\"valid_target_types\\\": [\\\"tosca.capabilities.Container\\\"]}\"','ef3f4a83-6736-495d-921d-e5359edf82ab'),
('be3c8f9b-6ee9-4aa5-9eea-a086c9c938ff','1.0','data_type','tosca.datatypes.network.NetworkInfo','\"{\\\"derived_from\\\": \\\"tosca.datatypes.Root\\\", \\\"description\\\": \\\"The Network type describes logical network information.\\\", \\\"properties\\\": {\\\"network_name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The name of the logical network. e.g., \\\\u201cpublic\\\\u201d, \\\\u201cprivate\\\\u201d, \\\\u201cadmin\\\\u201d. etc.\\\"}, \\\"network_id\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The unique ID of for the network generated by the network provider.\\\"}, \\\"addresses\\\": {\\\"type\\\": \\\"list\\\", \\\"description\\\": \\\"The list of IP addresses assigned from the underlying network.\\\", \\\"entry_schema\\\": {\\\"type\\\": \\\"string\\\"}}}}\"','24064643-f88b-4f8d-9c15-beaf43e04728'),
('c0440c98-a0a7-4f64-8bb1-f32f6fb95bef','1.0','artifact_type','tosca.artifacts.File','\"{\\\"derived_from\\\": \\\"tosca.artifacts.Root\\\", \\\"description\\\": \\\"This artifact type is used when an artifact definition needs to have its associated file simply treated as a file and no special handling/handlers are invoked.\\\\n\\\"}\"','32e6275f-8d7b-4449-b0f9-36d4d42e3833'),
('c5d5a2ad-831e-4ca1-852f-6f7f2626a493','1.0','artifact_type','tosca.artifacts.Implementation.Python','\"{\\\"derived_from\\\": \\\"tosca.artifacts.Implementation\\\", \\\"description\\\": \\\"Artifact for the interpreted Python language\\\", \\\"mime_type\\\": \\\"application/x-python\\\", \\\"file_ext\\\": [\\\"py\\\"]}\"','32e6275f-8d7b-4449-b0f9-36d4d42e3833'),
('cc84dac5-fecf-4402-a4d0-fd9ff00484ea','1.0','node_type','tosca.nodes.Root','\"{\\\"description\\\": \\\"This is the default (root) TOSCA Node Type that all other TOSCA nodes should extends.  This allows all TOSCA nodes to have a consistent set of features for modeling and management (e.g, consistent definitions for requirements, capabilities, and lifecycle interfaces).\\\\n\\\", \\\"attributes\\\": {\\\"tosca_id\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"A unique identifier of the realized instance of a Node Template that derives from any TOSCA normative type.\\\"}, \\\"tosca_name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"This attribute reflects the name of the Node Template as defined in the TOSCA service template.  This name is not unique to the realized instance model of corresponding deployed application as each template in the model can result in one or more instances (e.g., scaled) when orchestrated to a provider environment.\\\\n\\\"}, \\\"state\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The state of the node instance. See section \\\\u201cNode States\\\\u201d for allowed values.\\\", \\\"default\\\": \\\"initial\\\"}}, \\\"requirements\\\": [{\\\"dependency\\\": {\\\"capability\\\": \\\"tosca.capabilities.Node\\\", \\\"node\\\": \\\"tosca.nodes.Root\\\", \\\"relationship\\\": \\\"tosca.relationships.DependsOn\\\", \\\"occurrences\\\": [0, \\\"UNBOUNDED\\\"]}}], \\\"capabilities\\\": {\\\"feature\\\": {\\\"type\\\": \\\"tosca.capabilities.Node\\\"}}, \\\"interfaces\\\": {\\\"Standard\\\": {\\\"type\\\": \\\"tosca.interfaces.node.lifecycle.Standard\\\"}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('cccd4f7d-d5f1-4d7f-954f-87727c32986d','1.0','data_type','null','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"ard.null\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('cfc08d20-44f9-4168-84c9-88454e778536','1.0','node_type','tosca.nodes.network.Port','\"{\\\"derived_from\\\": \\\"tosca.nodes.Root\\\", \\\"description\\\": \\\"The TOSCA Port node represents a logical entity that associates between Compute and Network normative types. The Port node type effectively represents a single virtual NIC on the Compute node instance.\\\\n\\\", \\\"attributes\\\": {\\\"ip_address\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The IP address would be assigned to the associated compute instance.\\\\n\\\"}}, \\\"properties\\\": {\\\"ip_address\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"Allow the user to set a fixed IP address. Note that this address is a request to the provider which they will attempt to fulfill but may not be able to dependent on the network the port is associated with.\\\\n\\\", \\\"required\\\": false}, \\\"order\\\": {\\\"type\\\": \\\"integer\\\", \\\"description\\\": \\\"The order of the NIC on the compute instance (e.g. eth2). Note: when binding more than one port to a single compute (aka multi vNICs) and ordering is desired, it is *mandatory* that all ports will be set with an order value and. The order values must represent a positive, arithmetic progression that starts with 0 (e.g. 0, 1, 2, ..., n).\\\\n\\\", \\\"required\\\": true, \\\"default\\\": 0, \\\"constraints\\\": [{\\\"greater_or_equal\\\": 0}]}, \\\"is_default\\\": {\\\"type\\\": \\\"boolean\\\", \\\"description\\\": \\\"Set is_default=true to apply a default gateway route on the running compute instance to the associated network gateway. Only one port that is associated to single compute node can set as default=true.\\\\n\\\", \\\"required\\\": false, \\\"default\\\": false}, \\\"ip_range_start\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"Defines the starting IP of a range to be allocated for the compute instances that are associated by this Port. Without setting this property the IP allocation is done from the entire CIDR block of the network.\\\\n\\\", \\\"required\\\": false}, \\\"ip_range_end\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"Defines the ending IP of a range to be allocated for the compute instances that are associated by this Port. Without setting this property the IP allocation is done from the entire CIDR block of the network.\\\\n\\\", \\\"required\\\": false}}, \\\"requirements\\\": [{\\\"link\\\": {\\\"capability\\\": \\\"tosca.capabilities.network.Linkable\\\", \\\"relationship\\\": \\\"tosca.relationships.network.LinksTo\\\"}}, {\\\"binding\\\": {\\\"capability\\\": \\\"tosca.capabilities.network.Bindable\\\", \\\"relationship\\\": \\\"tosca.relationships.network.BindsTo\\\"}}]}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('d2e267f6-9b01-42c6-bb89-3f73c322a62d','1.0','artifact_type','tosca.artifacts.Root','\"{\\\"description\\\": \\\"The TOSCA Artifact Type all other TOSCA Artifact Types derive from\\\"}\"','32e6275f-8d7b-4449-b0f9-36d4d42e3833'),
('d46efdce-0534-4ef5-b706-8d5220f7b9e3','1.0','capability_type','tosca.capabilities.Node','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Root\\\", \\\"description\\\": \\\"The Node capability indicates the base capabilities of a TOSCA Node Type.\\\"}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('d80a9264-3be4-42ca-9e66-5369933ba2ed','1.0','node_type','tosca.nodes.DBMS','\"{\\\"derived_from\\\": \\\"tosca.nodes.SoftwareComponent\\\", \\\"description\\\": \\\"The TOSCA DBMS node represents a typical relational, SQL Database Management System software component or service.\\\", \\\"properties\\\": {\\\"root_password\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"the optional root password for the DBMS service\\\", \\\"required\\\": false}, \\\"port\\\": {\\\"type\\\": \\\"integer\\\", \\\"description\\\": \\\"the port the DBMS service will listen to for data and requests\\\", \\\"required\\\": false}}, \\\"capabilities\\\": {\\\"host\\\": {\\\"type\\\": \\\"tosca.capabilities.Compute\\\", \\\"valid_source_types\\\": [\\\"tosca.nodes.Database\\\"]}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('da5ff072-0aed-42de-b628-0556990474e7','1.0','relationship_type','tosca.relationships.RoutesTo','\"{\\\"derived_from\\\": \\\"tosca.relationships.ConnectsTo\\\", \\\"description\\\": \\\"This type represents an intentional network routing between two Endpoints in different networks.\\\", \\\"valid_target_types\\\": [\\\"tosca.capabilities.Endpoint\\\"]}\"','ef3f4a83-6736-495d-921d-e5359edf82ab'),
('db6d73e7-052b-4fde-90b2-62ae3534d9a8','1.0','capability_type','tosca.capabilities.network.Bindable','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Node\\\", \\\"description\\\": \\\"A node type that includes the Bindable capability indicates that it can be bound to a logical network association via a network port.\\\"}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('de264d5d-ef14-4639-aefb-e5f97455a787','1.0','data_type','map','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"ard.map\\\", \\\"specification.citation\\\": \\\"[TOSCA-Simple-Profile-YAML-v1.3]\\\", \\\"specification.location\\\": \\\"3.3.5\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('eb45816e-5e1b-4733-842e-b7c3c0197f2f','1.0','data_type','string','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"ard.string\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('eca84a82-cc93-4703-9037-69fa077a8fa4','1.0','artifact_type','tosca.artifacts.template','\"{\\\"derived_from\\\": \\\"tosca.artifacts.Root\\\", \\\"description\\\": \\\"TOSCA base type for template artifacts\\\"}\"','32e6275f-8d7b-4449-b0f9-36d4d42e3833'),
('ef687b8a-af46-4c63-9964-ee496491392d','1.0','data_type','scalar-unit.bitrate','\"{\\\"metadata\\\": {\\\"puccini.type\\\": \\\"scalar-unit.bitrate\\\", \\\"specification.citation\\\": \\\"[TOSCA-Simple-Profile-YAML-v1.3]\\\", \\\"specification.location\\\": \\\"3.3.6.7\\\"}}\"','9601947c-ec8d-43d7-81d3-424dad712793'),
('f03976a3-3a13-43ea-8460-c29a93311ef0','1.0','relationship_type','tosca.relationships.DependsOn','\"{\\\"derived_from\\\": \\\"tosca.relationships.Root\\\", \\\"description\\\": \\\"This type represents a general dependency relationship between two nodes.\\\", \\\"valid_target_types\\\": [\\\"tosca.capabilities.Node\\\"]}\"','ef3f4a83-6736-495d-921d-e5359edf82ab'),
('f4ce612e-3f30-4026-9420-a92355b077cf','1.0','capability_type','tosca.capabilities.Storage','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Root\\\", \\\"description\\\": \\\"The Storage capability, when included on a Node Type or Template definition, indicates that the node can provide a named storage location with specified size range.\\\", \\\"properties\\\": {\\\"name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The otional name (or identifier) of a specific storage resource.\\\", \\\"required\\\": false}}}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('f72609b5-c13a-4cb1-b09b-40b43e297c8a','1.0','capability_type','tosca.capabilities.Endpoint.Admin','\"{\\\"derived_from\\\": \\\"tosca.capabilities.Endpoint\\\", \\\"description\\\": \\\"This is the default TOSCA type that should be used or extended to define a specialized administrator endpoint capability.\\\", \\\"properties\\\": {\\\"secure\\\": {\\\"type\\\": \\\"boolean\\\", \\\"default\\\": true, \\\"constraints\\\": [{\\\"equal\\\": true}]}}}\"','c4f1b01e-17ad-4d68-9d99-40b78063588b'),
('fa76ef5b-9de0-4b6f-a49f-7526101fa498','1.0','relationship_type','tosca.relationships.network.BindsTo','\"{\\\"derived_from\\\": \\\"tosca.relationships.DependsOn\\\", \\\"description\\\": \\\"This type represents a network association relationship between Port and Compute node types.\\\\n\\\", \\\"valid_target_types\\\": [\\\"tosca.capabilities.network.Bindable\\\"]}\"','ef3f4a83-6736-495d-921d-e5359edf82ab'),
('fc6a4f1c-1377-46e5-81e6-ebd9095cd363','1.0','artifact_type','tosca.artifacts.Implementation','\"{\\\"derived_from\\\": \\\"tosca.artifacts.Root\\\", \\\"description\\\": \\\"TOSCA base type for implementation artifacts\\\"}\"','32e6275f-8d7b-4449-b0f9-36d4d42e3833'),
('fdf30be5-439c-4c93-90fe-d198dd2fa81e','1.0','node_type','tosca.nodes.network.Network','\"{\\\"derived_from\\\": \\\"tosca.nodes.Root\\\", \\\"description\\\": \\\"The TOSCA Network node represents a simple, logical network service.\\\\n\\\", \\\"attributes\\\": {\\\"segmentation_id\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The actual segmentation_id that is been assigned to the network by the underlying cloud infrastructure.\\\\n\\\"}}, \\\"properties\\\": {\\\"ip_version\\\": {\\\"type\\\": \\\"integer\\\", \\\"description\\\": \\\"The IP version of the requested network.\\\\n\\\", \\\"required\\\": false, \\\"default\\\": 4, \\\"constraints\\\": [{\\\"valid_values\\\": [4, 6]}]}, \\\"cidr\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The cidr block of the requested network.\\\\n\\\", \\\"required\\\": false}, \\\"start_ip\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The IP address to be used as the 1st one in a pool of addresses derived from the cidr block full IP range.\\\\n\\\", \\\"required\\\": false}, \\\"end_ip\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The IP address to be used as the last one in a pool of addresses derived from the cidr block full IP range.\\\\n\\\", \\\"required\\\": false}, \\\"gateway_ip\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The gateway IP address.\\\\n\\\", \\\"required\\\": false}, \\\"network_name\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"An Identifier that represents an existing Network instance in the underlying cloud infrastructure \\\\u2013 OR \\\\u2013 be used as the name of the new created network. . If network_name is provided along with network_id they will be used to uniquely identify an existing network and not creating a new one, means all other possible properties are not allowed. . network_name should be more convenient for using. But in case that network name uniqueness is not guaranteed then one should provide a network_id as well.\\\\n\\\", \\\"required\\\": false}, \\\"network_id\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"An Identifier that represents an existing Network instance in the underlying cloud infrastructure. This property is mutually exclusive with all other properties except network_name. . Appearance of network_id in network template instructs the Tosca container to use an existing network instead of creating a new one. . network_name should be more convenient for using. But in case that network name uniqueness is not guaranteed then one should add a network_id as well. . network_name and network_id can be still used together to achieve both uniqueness and convenient.\\\\n\\\", \\\"required\\\": false}, \\\"segmentation_id\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"A segmentation identifier in the underlying cloud infrastructure (e.g., VLAN id, GRE tunnel id). If the segmentation_id is specified, the network_type or physical_network properties should be provided as well.\\\\n\\\", \\\"required\\\": false}, \\\"network_type\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"Optionally, specifies the nature of the physical network in the underlying cloud infrastructure. Examples are flat, vlan, gre or vxlan. For flat and vlan types, physical_network should be provided too.\\\\n\\\", \\\"required\\\": false}, \\\"physical_network\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"Optionally, identifies the physical network on top of which the network is implemented, e.g. physnet1. This property is required if network_type is flat or vlan.\\\\n\\\", \\\"required\\\": false}, \\\"dhcp_enabled\\\": {\\\"type\\\": \\\"boolean\\\", \\\"description\\\": \\\"Indicates the TOSCA container to create a virtual network instance with or without a DHCP service.\\\\n\\\", \\\"required\\\": false, \\\"default\\\": true}}, \\\"capabilities\\\": {\\\"link\\\": {\\\"type\\\": \\\"tosca.capabilities.network.Linkable\\\"}}}\"','0fb68c2e-0b52-43cc-b437-855dc7515483'),
('ff03bd77-e71a-4b41-a66e-4fe5532dd9bb','1.0','data_type','tosca.datatypes.network.PortSpec','\"{\\\"derived_from\\\": \\\"tosca.datatypes.Root\\\", \\\"description\\\": \\\"The PortSpec type describes port specifications for a network connection.\\\", \\\"properties\\\": {\\\"protocol\\\": {\\\"type\\\": \\\"string\\\", \\\"description\\\": \\\"The required protocol used on the port.\\\", \\\"required\\\": true, \\\"default\\\": \\\"tcp\\\", \\\"constraints\\\": [{\\\"valid_values\\\": [\\\"udp\\\", \\\"tcp\\\", \\\"igmp\\\"]}]}, \\\"source\\\": {\\\"type\\\": \\\"tosca.datatypes.network.PortDef\\\", \\\"description\\\": \\\"The optional source port.\\\", \\\"required\\\": false}, \\\"source_range\\\": {\\\"type\\\": \\\"range\\\", \\\"description\\\": \\\"The optional range for the source port.\\\", \\\"required\\\": false, \\\"constraints\\\": [{\\\"in_range\\\": [1, 65535]}]}, \\\"target\\\": {\\\"type\\\": \\\"tosca.datatypes.network.PortDef\\\", \\\"description\\\": \\\"The optional target port.\\\", \\\"required\\\": false}, \\\"target_range\\\": {\\\"type\\\": \\\"range\\\", \\\"description\\\": \\\"The optional range for the target port.\\\", \\\"required\\\": false, \\\"constraints\\\": [{\\\"in_range\\\": [1, 65535]}]}}}\"','24064643-f88b-4f8d-9c15-beaf43e04728');
/*!40000 ALTER TABLE `type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type_header`
--

DROP TABLE IF EXISTS `type_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `type_header` (
  `id` char(36) NOT NULL,
  `template_version` char(255) NOT NULL,
  `template_name` char(255) NOT NULL,
  `tosca_definitions_version` char(255) NOT NULL,
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `template_author` char(255) NOT NULL,
  `imports` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_header_complex_pk` (`template_name`,`template_author`,`template_version`,`tosca_definitions_version`) USING HASH,
  CONSTRAINT `imports` CHECK (json_valid(`imports`)),
  CONSTRAINT `metadata` CHECK (json_valid(`metadata`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type_header`
--

LOCK TABLES `type_header` WRITE;
/*!40000 ALTER TABLE `type_header` DISABLE KEYS */;
INSERT INTO `type_header` VALUES
('0fb68c2e-0b52-43cc-b437-855dc7515483','1.3.0','tosca-normative-node-types','tosca_simple_yaml_1_3','{}','TOSCA TC','[\"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-data-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-capability-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-interface-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-relationship-types/1.3.0/raw\"]'),
('1d537788-bb3d-4f4e-bce5-f267082a6626','1.3.0','tosca-normative-types','tosca_simple_yaml_1_3','{}','TOSCA TC','[\"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-data-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-artifact-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-capability-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-interface-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-relationship-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-node-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-policy-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-group-types/1.3.0/raw\"]'),
('24064643-f88b-4f8d-9c15-beaf43e04728','1.3.0','tosca-normative-data-types','tosca_simple_yaml_1_3','{}','TOSCA TC','[\"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/Tal Liron/non-normative-puccini-implicit-types/1.0.0/raw\"]'),
('32e6275f-8d7b-4449-b0f9-36d4d42e3833','1.3.0','tosca-normative-artifact-types','tosca_simple_yaml_1_3','{}','TOSCA TC','[]'),
('3efa2dea-9690-4545-894d-959c532774ad','1.3.0','tosca-normative-group-types','tosca_simple_yaml_1_3','{}','TOSCA TC','[]'),
('9601947c-ec8d-43d7-81d3-424dad712793','1.0.0','non-normative-puccini-implicit-types','tosca_simple_yaml_1_3','{}','Tal Liron','[]'),
('9cb538f0-d864-4e4c-88e1-fc033f4a38ef','1.3.0','tosca-normative-policy-types','tosca_simple_yaml_1_3','{}','TOSCA TC','[]'),
('a35fbf65-ca8d-4f88-b0bf-6930f2e51cdd','1.3.0','tosca-normative-interface-types','tosca_simple_yaml_1_3','{}','TOSCA TC','[]'),
('c4f1b01e-17ad-4d68-9d99-40b78063588b','1.3.0','tosca-normative-capability-types','tosca_simple_yaml_1_3','{}','TOSCA TC','[\"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-data-types/1.3.0/raw\"]'),
('ef3f4a83-6736-495d-921d-e5359edf82ab','1.3.0','tosca-normative-relationship-types','tosca_simple_yaml_1_3','{}','TOSCA TC','[\"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-data-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-capability-types/1.3.0/raw\", \"http://localhost:4000/type-storage/tosca_simple_yaml_1_3/TOSCA TC/tosca-normative-interface-types/1.3.0/raw\"]');
/*!40000 ALTER TABLE `type_header` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `value_storage`
--

DROP TABLE IF EXISTS `value_storage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `value_storage` (
  `id` char(36) NOT NULL,
  `value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `value` CHECK (json_valid(`value`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `value_storage`
--

LOCK TABLES `value_storage` WRITE;
/*!40000 ALTER TABLE `value_storage` DISABLE KEYS */;
/*!40000 ALTER TABLE `value_storage` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-31 15:13:49
