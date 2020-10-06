# accounting_app_gl.py

"""Routes for GL processes"""

from flask import (Blueprint,
                   render_template,
                   redirect,
                   url_for,
                   request,
                   flash,
                   )


from ... database.db_connection import (create_connection,
                                        execute_query,
                                        execute_read_query,
                                        )

from ... database.sql_queries.queries_read import (select_all,
                                                   select_batch_available,
                                                   # select_entity_name_by_id,
                                                   select_batch_by_row_id,
                                                   batch_total,
                                                   )

from ... database.sql_queries.queries_insert import (insert_new_batch_name,
                                                     insert_new_je_transaction,
                                                     batch_load_je_file,
                                                     batch_load_insert,
                                                     )

from . forms import (JournalEntryForm,
                     #JournalUpdateForm,
                     BatchEntryForm,
                     UploadFileForm,
                     )

# Table names set up

gl_table = 'general_ledger'
gl_staging = 'general_ledger_staging'
journal_batch_table = 'journal_batch'   # JE batch table
journal_table = 'journal'
entity_table = 'entity'   # Entity table

accounting_app_journals_bp = Blueprint('accounting_app_journals_bp',
                                       __name__,
                                       template_folder='templates',
                                       static_folder='static',
                                       static_url_path='accounting_app')

accounting_app_gl_bp = Blueprint('accounting_app_gl_bp',
                                 __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 static_url_path='accounting_app')

###############################################################################


@accounting_app_gl_bp.route('/gl/hello_there_gl', methods=['GET', 'POST'])
def hello_there_gl():
    return '<h1>Hello There! You are in a GL page.</h1>'


@accounting_app_gl_bp.route('/gl/gl_strobe', methods=['GET', 'POST'])
def gl_strobe():

    """Endpoint to reference while building the pages and functions related to
    GL (general ledger) entries.
    """
    marker = 'Test Value Golf Lima'

    return render_template('gl/gl_strobe.html',
                           marker=marker,
                           )


@accounting_app_gl_bp.route('/gl/general_ledger/<batch_row_id>', methods=['GET', 'POST'])
def general_ledger(batch_row_id):

    """Route for GL review of queries related to posting a batch of
    journal entries to the general ledger.
    """

    return f'<h1>Check GL Landing {batch_row_id}</h1>'

    # print(f"TROUBLESHOOTING _ *********************************************")
    # print(f"TROUBLESHOOTING _ *********************************************")
    # # Get the batch DR/CR totals
    # (check_batch, check_DR, check_CR) = batch_total(batch_id)

    # print(f"CHECK ::::::::::: {check_batch}")
    # print(f"CHECK ::::::::::: {check_DR}")
    # print(f"CHECK ::::::::::: {check_CR}")

    # # Get the batch row id
    # batch_row_id = get_journal_batch_row_id(batch_id)
    # print(f"CHECK !!!!!!!!!!!!!!!!! {batch_row_id}")

    # count_check = Xref_Batch_GL_Staging.query.filter_by(batch_row_id=batch_row_id).count()

    # print(f"xref batch staging check: {count_check}")
    # print("")

    # # Get the batch row as an object from the batch_journal table
    # je_batch_id = JournalBatch.query.filter_by(journal_batch_row_id=batch_row_id).first()

    # if count_check == 0:

    #     # batch_summary_gl aggregates the journal entries for the batch_id
    #     # and inserts them into a gl staging table.
    #     query_status, journals_summary_list = batch_summary_gl(batch_id)
    # else:
    #     # Grab existing staged rows
    #     query_status, journals_summary_list = get_staged_jes(batch_id)

    # for row_data in journals_summary_list:
    #     print(f"journals_summary_list >>> {row_data}")

    # je_batch_stage = Journal.query.filter_by(journal_batch_id=je_batch_id.journal_batch_id)

    # gl_stage_status, gl_stage = batch_get_gl_staging(batch_id)

    # # REMOVE AFTER TESTING

    # for _ in gl_stage:

    #     print(f"gl_stage row ++++++ {_}")

    # return render_template('accounting/general_ledger.html',
    #                        je_batch_stage=je_batch_stage,
    #                        check_batch=check_batch,
    #                        check_DR=check_DR,
    #                        check_CR=check_CR,
    #                        query_status=query_status,
    #                        journals_summary_list=journals_summary_list,
    #                        gl_stage=gl_stage,
    #                        batch_id=batch_id,
    #                        )


# Use code from this section to post batch to GL when ready

# @accounting_app_journals_bp.route('/journals/journal_loader_batch_review/<int:batch_row_id>', methods=['GET', 'POST'])
# def journal_loader_batch_review(batch_row_id):

#     """Review JE's for a batch and mark ready to post to GL.
#     """

#     # Get row for corresponding batch_row_id
#     journal_batch_row = select_batch_by_row_id(journal_batch_table, batch_row_id)

#     # Get batch_name  for corresponding batch_row_id
#     batch_name = journal_batch_row[0][1]

#     # Get rows for corresponding batch_row_id in journal table
#     batch_jes = select_batch_by_row_id(journal_table, batch_row_id)

#     print('+' * 50)
#     for _ in batch_jes:
#       print(f'{_}')
#     print('+' * 50)
#     # Get gl status for corresponding batch_row_id
#     journal_batch_gl_status = journal_batch_row[0][6]

#     (batch_row_id, total_DR, total_CR) = batch_total(batch_row_id)

#     return render_template('journals/batch_review.html',
#                            batch_jes=batch_jes,
#                            batch_row_id=batch_row_id,
#                            batch_name=batch_name,
#                            total_DR=total_DR,
#                            total_CR=total_CR,
#                            batch_gl_status=journal_batch_gl_status,
#                            )
