import unicodecsv
from cumulusci.tasks.bulkdata.extract import ExtractData as BaseExtractData
from cumulusci.tasks.bulkdata.utils import fields_for_mapping
class ExtractData(BaseExtractData):
    def _soql_for_mapping(self, mapping):
        sf_object = mapping["sf_object"]
        fields = []
        if not mapping["oid_as_pk"]:
            fields.append("Id")
        fields += [field["sf"] for field in fields_for_mapping(mapping)]
        soql = "SELECT {fields} FROM {sf_object}".format(
            **{"fields": ", ".join(fields), "sf_object": sf_object}
        )
        where = []
        #import pdb; pdb.set_trace()
        if "record_type" in mapping:
            where.append(
                "RecordType.DeveloperName = '{}'".format(
                    mapping["record_type"]
                )
            )
        if "where" in mapping:
            where.extend(mapping["where"])
        if where:
            soql += " WHERE {}".format(" AND ".join(where))
        return soql

    def _sql_bulk_insert_from_csv(self, conn, table, columns, data_file):
        if conn.dialect.name in ("postgresql", "psycopg2"):
            # psycopg2 (the postgres driver) supports COPY FROM
            # to efficiently bulk insert rows in CSV format
            with conn.connection.cursor() as cursor:
                cursor.copy_expert(
                    "COPY {} ({}) FROM STDIN WITH (FORMAT CSV)".format(
                        table, ",".join(columns)
                    ),
                    data_file,
                )
        else:
            # For other db drivers we need to use standard SQL
            # -- this is optimized for ease of implementation
            # rather than performance and may need more work.
            reader = unicodecsv.DictReader(data_file, columns)
            table = self.metadata.tables[table]
            rows = list(reader)
            if rows:
                chunk_size = 10
                for i in range(0, len(rows), chunk_size):
                    conn.execute(table.insert().values(rows[i:i+chunk_size]))
        self.session.flush()