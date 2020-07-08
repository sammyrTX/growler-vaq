# queries_to_migrate.py

"""Replicate and decompose the sql queries functions listed below from
rhino-striker into growler-vaq.
"""

# List of query functions from SQL_Functions.py from rhino-striker

# cat SQL_Functions.py |grep def
# def get_journal_batch_row_id(journal_batch_id):
# def get_period(gl_date):
# def batch_total(batch_id):
# def batch_load_je_file(filename):
# def batch_load_review(batch_id):
# def batch_load_insert(batch_id):
# def gl_staging_insert(batch_id, journals_summary_list):
# def batch_summary_gl(batch_id):
# def batch_get_gl_staging(batch_id):
# def batch_staging_to_gl_insert(batch_id):
# def update_batch_gl_status(batch_id, status):
# def clear_gl_staging(batch_id):
# def get_staged_jes(batch_id):
# def gl_trial_balance(period):
# def timestamp_generator():
# def timestamp_session():
