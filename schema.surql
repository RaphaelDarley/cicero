USE NS cicero;
USE DB cicero;

DEFINE TABLE fact TYPE NORMAL SCHEMAFULL;
DEFINE FIELD data ON fact TYPE string;
DEFINE FIELD source ON fact TYPE option<string>;
DEFINE FIELD embed ON fact TYPE array<float, 1024> ASSERT array::len($value) = 1024;
DEFINE INDEX embed_index ON fact FIELDS embed MTREE DIMENSION 1024 DIST COSINE TYPE f32;

DEFINE TABLE proves TYPE RELATION FROM fact TO fact SCHEMAFULL;
DEFINE FIELD reason on proves TYPE option<string>;

DEFINE FUNCTION fn::add_k_v($obj: object, $key: any, $val: any) {

	LET $es = object::entries($obj);

	LET $new_es = array::append($es, [
		$key,
		$val
	]);

	RETURN object::from_entries($new_es);

}
	PERMISSIONS FULL
;

DEFINE FUNCTION fn::get_tree($root: record<fact>) {

	LET $rels = (SELECT VALUE <-proves FROM ONLY $root);

	LET $out = (SELECT reason, in.id AS id, in.data AS data, in.source as source, fn::get_tree(in.id) AS related FROM $rels);

	RETURN $out;

}
	PERMISSIONS FULL
;