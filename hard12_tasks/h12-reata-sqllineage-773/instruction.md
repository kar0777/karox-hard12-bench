You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

DDL fragments leaking into column names for sparksql

**Describe the bug**

**SQL**
1.test sql here. [dws_domain_pl_map_df .sql]
```sql
CREATE TABLE `dws.dws_domain_pl_map_df`(
   `domain_eng` string COMMENT 'dd',
   `domain` string COMMENT '',
   `platform_id` string COMMENT '',
   `platform_name` string COMMENT '',
   `center_id` string COMMENT '',
   `center_name` string COMMENT '',
   `etl_dt` string COMMENT '')
 COMMENT ''
 PARTITIONED BY (
   `bus_dt` string COMMENT '')
 ;
 
insert overwrite table dws.dws_domain_pl_map_df partition (bus_dt)
SELECT
       distinct
       case when domain = 'ee'              then 'tv'
            when domain = 'dd'          then 'radio'
            else ''
       end AS domain_eng
      ,domain
      ,platform_id
      ,platform_name
      ,platform_center_id as center_id
      ,platform_center_name as center_name
      ,current_timestamp()           as etl_dt         
      ,'${bus_dt}'                   as bus_dt          
 from dws.dws_manu_detail_info
where bus_dt = '${bus_dt}'
;
```



2.test python here.
```python
from sqllineage.core.metadata.dummy import DummyMetaDataProvider
from sqllineage.core.metadata.sqlalchemy import SQLAlchemyMetaDataProvider
from sqllineage.core.metadata_provider import MetaDataProvider
from sqllineage.runner import LineageRunner


def sqllineage_test_file(filepath, meta: MetaDataProvider = DummyMetaDataProvider()):
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    runner = LineageRunner(
        sql=sql_content,
        dialect='sparksql',
        metadata_provider=meta,
        verbose=True,
        silent_mode=True
    )

    # runner.print_table_lineage()
    runner.print_column_lineage()

if __name__ == '__main__':
    file = 'dws_domain_pl_map_df .sql'
    sqllineage_test_file(file)
```



**Expected behavior**
dws.dws_domain_pl_map_df.bus_dt
dws.dws_domain_pl_map_df.center_id <- dws.dws_manu_detail_info.platform_center_id
dws.dws_domain_pl_map_df.center_name <- dws.dws_manu_detail_info.platform_center_name
dws.dws_domain_pl_map_df.domain <- dws.dws_manu_detail_info.domain
dws.dws_domain_pl_map_df.domain_eng <- dws.dws_manu_detail_info.domain
dws.dws_domain_pl_map_df.etl_dt <- dws.dws_manu_detail_info.${bus_dt}
dws.dws_domain_pl_map_df.etl_dt <- dws.dws_manu_detail_info.current_timestamp()
dws.dws_domain_pl_map_df.platform_id <- dws.dws_manu_detail_info.platform_id
dws.dws_domain_pl_map_df.platform_name <- dws.dws_manu_detail_info.platform_name


**Actual behavior**
dws.dws_domain_pl_map_df.bus_dt
dws.dws_domain_pl_map_df.center_id <- dws.dws_manu_detail_info.platform_center_id
dws.dws_domain_pl_map_df.center_id` string COMMENT 
dws.dws_domain_pl_map_df.center_name <- dws.dws_manu_detail_info.platform_center_name
dws.dws_domain_pl_map_df.center_name` string COMMENT 
dws.dws_domain_pl_map_df.domain <- dws.dws_manu_detail_info.domain
dws.dws_domain_pl_map_df.domain_eng <- dws.dws_manu_detail_info.domain
dws.dws_domain_pl_map_df.domain_eng` string COMMENT 'dd
dws.dws_domain_pl_map_df.domain` string COMMENT 
dws.dws_domain_pl_map_df.etl_dt` string COMMENT 
dws.dws_domain_pl_map_df.platform_id <- dws.dws_manu_detail_info.platform_id
dws.dws_domain_pl_map_df.platform_id` string COMMENT 
dws.dws_domain_pl_map_df.platform_name <- dws.dws_manu_detail_info.platform_name
dws.dws_domain_pl_map_df.platform_name` string COMMENT 


**Python version (available via `python --version`)**
 - 3.10.0
 - 3.11.0
 - 3.12.0
 - 3.13.0
 - 3.14.0
 - etc.

**SQLLineage version (available via `sqllineage --version`):**
 - 1.5.6

** Temporary solution**
Modify the “sqllineage\core\parser\sqlfluff\extractors\create_insert.py” file.some sub_segment have no child with "identifier", then we need to  determine raw_segment of sub_segment is type of "identifier".

Modify function:
def extract(
        self,
        statement: BaseSegment,
        context: AnalyzerContext,
    ) -> SubQueryLineageHolder:


add code:
```python
            elif segment.type == "bracketed":
                # In case of bracketed column reference, add these target columns to holder
                # so that when we compute the column level lineage
                # we keep these columns into consideration
                sub_segments = list_child_segments(segment)
                if all(
                    sub_segment.type in ["column_reference", "column_definition"]
                    for sub_segment in sub_segments
                ):
                    # target columns only apply to bracketed column_reference and column_definition
                    columns = []
                    for sub_segment in sub_segments:
                        if sub_segment.type == "column_definition":
                            if identifier := sub_segment.get_child("identifier"):
                                sub_segment = identifier
                            
                           #-------- here is my add code ---------------
                            else:
                                 for rsegment in sub_segment.get_raw_segments():
                                    if rsegment.type == "identifier":
                                        sub_segment = rsegment
                                        break
                          #-------- here is my add code ---------------

                        columns.append(SqlFluffColumn.of(sub_segment))
                    holder.add_write_column(*columns)
```


