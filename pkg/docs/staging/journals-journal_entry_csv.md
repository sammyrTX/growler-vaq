## Journal entry csv file fields

Below are the required fields for creating a journal entry load file
in csv format. File must include header row. Use spreadsheet application
to create and save as a comma delimited file with a csv extension.

Field Name              Data Type                      Description
journal_id              Integer                        Leave blank
journal_date            Text (20 Characters)           Transaction date
account_number          Integer                        Account number
department_number       Integer                        Department number
journal_entry_type      Integer                        Journal entry type
journal_debit           Number (float)                 Debit amount
journal_credit          Number (float)                 Credit amount
journal_description     Text (100 Characters)          Journal entry description
journal_reference       Text (30 Characters)           Journal entry reference info
journal_batch_row_id    Integer                        Row ID of Journal Batch
gl_post_reference       Text (20 Characters)           General Ledger status
journal_entity          Integer                        Row ID of entity
journal_currency        Integer                        Row ID of currency


## Field conventions
journal_date:          YYYY-MM-DD  e.g. 2020-01-29


### Sample header and row data

journal_id,journal_date,account_number,department_number,journal_entry_type,journal_debit,journal_credit,journal_description,journal_reference,journal_batch_row_id,gl_post_reference,journal_entity,journal_currency
,2019-11-01,6070,500,99,589.97,0,test transaction v1 – expense-00,ref JE-LOAD-TEST-06,2,,1,1
,2019-11-01,6070,500,99,46.33,0,test transaction v1 – expense-01,ref JE-LOAD-TEST-06,2,,1,1
,2019-11-05,6070,500,99,901.33,0,test transaction v1 – expense-02,ref JE-LOAD-TEST-06,2,,1,1