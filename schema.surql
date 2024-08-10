USE NS cicero;
USE DB cicero;

DEFINE TABLE fact TYPE NORMAL SCHEMAFULL;
DEFINE FIELD data ON fact TYPE string;
DEFINE FIELD embed ON fact TYPE array<float, 1024> ASSERT array::len($value) = 1024;
DEFINE FIELD embed_index ON fact FIELDS embed MTREE DIMENSION 1024 DIST COSINE;


DEFINE TABLE related TYPE RELATION FROM fact TO fact SCHEMAFULL;
DEFINE FIELD kind on related TYPE string ASSERT $value INSIDE ["proves", "disproves", "unrelated"]; 


-- DEFINE FUNCTION fn::get_provenance($root: record<fact>) {
--     LET $rel = $root<-related<- 
    
-- };