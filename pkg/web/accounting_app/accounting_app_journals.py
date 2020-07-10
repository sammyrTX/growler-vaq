# accounting_app_journals.py

"""Routes for Journals"""

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

from ... database.sql_queries.queries_read import select_all

accounting_app_journals_bp = Blueprint('accounting_app_journals_bp',
                                       __name__,
                                       template_folder='templates',
                                       static_folder='static',
                                       static_url_path='accounting_app')


###############################################################################


@accounting_app_journals_bp.route('/journals/batch_load_file', methods=['GET', 'POST'])
def batch_load_file():

    """Prompt for a file location of the load file containing journal entries.
    Select filename for journal entry csv file to be inserted into journals table. Files need to be saved in the je_csv_data folder within the web app root folder.
    """

    # form = UploadFileForm()

    # if form.validate_on_submit():

    #     filename = form.filename.data

    #     load_file = batch_load_je_file(filename)

    #     if load_file == "LOAD OK":
    #         _batch = JournalBatch.query.filter_by(journal_batch_row_id=batch_row_id).first()

    #         _batch_id = _batch.journal_batch_id

    #         print(f"CHECK _batch_id: {_batch_id} <<<<<<<<<<<<<<<<<")

    #         load_status = batch_load_insert(_batch_id)

    #         if load_status == "INSERT COMPLETE":

    #             return redirect(url_for('journals.review_batch', batch_row_id=batch_row_id))
    #         else:

    #             return render_template('accounting/load_error.html')

    # _batch = JournalBatch.query.filter_by(journal_batch_row_id=batch_row_id).first()

    # _batch_id = _batch.journal_batch_id

    # _batch_jes = Journal.query.filter_by(journal_batch_id=_batch.journal_batch_id)

    # (batch_id__, total_DR, total_CR) = batch_total(_batch_id)

    _batch = 'Test JE Batch ID'

    _batch_id = '_batch.journal_batch_id'

    _batch_jes = 'aaa'

    (batch_id__, total_DR, total_CR) = (1000, -1000, 0)

    # return render_template('accounting_app/journals/batch_load_file.html',
    return render_template('journals/batch_load_file.html',
                           # form=form,
                           _batch_jes=_batch_jes,
                           _batch_id=_batch_id,
                           batch_id__=batch_id__,
                           total_DR=total_DR,
                           total_CR=total_CR,
                           )
#

# @accounting_app_bp.route('/chart_of_accounts')
# def chart_of_accounts():

#     """Show list of accounts in chart of accounts table.
#     """

#     coa = select_all('chart_of_accounts')

#     return render_template('accounting_app/chart_of_accounts.html',
#                            coa=coa,
#                            )

###############################################################################
# ###############################################################################
# # Code from rhino-tracker to be migrated as required to growler-vaq

# # acctg_system/views.py

# from flask import (render_template,
#                    url_for,
#                    flash,
#                    redirect,
#                    request,
#                    Blueprint,
#                    )

# from flask_login import current_user, login_required
# from accounting_app import db
# from accounting_app.models import BlogPost
# from accounting_app.blog_posts.forms import BlogPostForm

# from accounting_app.models import (Journal,
#                                    JournalTest,
#                                    Departments,
#                                    Entity,
#                                    Currency,
#                                    JournalBatch,
#                                    ChartOfAccounts,
#                                    GeneralLedger_Staging,
#                                    Xref_Batch_GL_Staging,
#                                    Periods,
#                                    )

# from sqlalchemy import (exc,
#                         or_,
#                         )

# from sqlalchemy.sql import (func,
#                             select,
#                             )

# from accounting_app.acctg_system.forms import (JournalEntryForm,
#                                                JournalUpdateForm,
#                                                BatchEntryForm,
#                                                UploadFileForm,
#                                                )

# from datetime import datetime

# from accounting_app.sql.SQL_Functions import (batch_total,
#                                               batch_load_je_file,
#                                               batch_load_insert,
#                                               timestamp_generator,
#                                               batch_summary_gl,
#                                               get_journal_batch_row_id,
#                                               batch_get_gl_staging,
#                                               batch_staging_to_gl_insert,
#                                               update_batch_gl_status,
#                                               clear_gl_staging,
#                                               get_staged_jes,
#                                               gl_trial_balance,  # *IN TESTING*
#                                               )

# ###############################################################################

# # Accounting System routes

# # Blueprints

# journals = Blueprint('journals', __name__)
# # journals = Blueprint('journaltest', __name__)

# ###############################################################################

# # ORM filter for date ranges (KEEP until implemented)

#     # print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')

#     # stuff3 = Journal.query.filter(Journal.journal_date.between('2020-01-01', '2020-12-31'))

#     # for items3 in stuff3:
#     #     print(f"{items3} | {items3.journal_date}| {items3.journal_id} | {items3.journal_debit} | {items3.journal_credit}")

# ###############################################################################

# # Routes

# @journals.route('/journaltest')  # , method=['GET', 'POST'])
# def journaltest():

#     journal_ck = Journal.query.all()

#     if journal_ck == []:

#         # Insert a row into the Journal table

#         newJE = Journal(#journal_id=110,
#                         journal_name="Sales",
#                         journal_date="01/05/2019",
#                         account_id=111,
#                         department_id=230,
#                         journal_entry_type=0,
#                         journal_amount=1000.00,
#                         journal_description="Sample Journal Entry",
#                         journal_reference="Test Ref",
#                         )

#         db.session.add(newJE)
#         db.session.commit()

#         # Test Page
#         return render_template('accounting/acctg_message.html')

#     return redirect(url_for('core.index'))

# ###############################################################################


# @journals.route('/journals')  # Next version, pass arg for specific journal
# def journal():

#     """List all journal entries. Only a few columns are provided."""

#     journal_tbl = Journal.query.all()
#     return render_template('accounting/journal.html',
#                            journal_tbl=journal_tbl,
#                            )

# ###############################################################################


# @journals.route('/entity_currency')  # Next version, pass arg for specific journal
# def entity_currency():

#     """Show rows for the entity and currency tables."""
#     entity_tbl = Entity.query.all()
#     currency_tbl = Currency.query.all()

#     return render_template('accounting/entity_currency.html',
#                            entity_tbl=entity_tbl,
#                            currency_tbl=currency_tbl,
#                            )

# ###############################################################################


# @journals.route('/message')  # TODO
# def message(flag):

#     """Test route. REMOVE when ready"""
#     if flag == "alpha":
#         return render_template('accounting/je_edit.html')

#     return render_template('accounting/acctg_message.html')

# ###############################################################################


# @journals.route('/load_error')  # TODO
# def load_error():

#     """If Journal Entry csv load file errors out, return this route"""

#     return render_template('accounting/load_error.html')

# ###############################################################################


# @journals.route('/je_entry/<int:journal_batch_row_id>', methods=['GET', 'POST'])
# # @login_required
# def je_entry(journal_batch_row_id):

#     """Journal Entry route. After selecting a specific batch, the user is
#     redirected to the Journal Entry page for the selected batch. Entity and
#     curremcy are hardcoded to the JE. Assumption is that a batch will only
#     be associated with a single entity and single currency.
#     """

#     form = JournalEntryForm()
#     dept_list = Departments.query.all()
#     account_list = ChartOfAccounts.query.all()

#     batch_ = JournalBatch.query.filter_by(journal_batch_row_id=journal_batch_row_id).first()

#     batch_id = batch_.journal_batch_id
#     batch_entity = batch_.journal_batch_entity
#     batch_currency = batch_.journal_batch_currency
#     entity_name = Entity.query.filter_by(entity_id=batch_entity).first()
#     currency__ = Currency.query.filter_by(currency_id=batch_currency).first()

#     #  Check form data here
#     print("############################################################")
#     print("### journal_batch_row_id:              ", journal_batch_row_id)
#     print("### batch_id:                      ", batch_id)
#     print("### entity_name:                   ", entity_name.entity_name)
#     print("### currency:                   ", currency__.currency_code)
#     print("### currency description:                   ", currency__.currency_description)
#     print("### batch_entity:                  ", batch_entity)
#     print("### batch_currency:                ", batch_currency)
#     print("### form.errors:                   ", form.errors)
#     print("### journal_name.data:             ", form.journal_name.data)
#     print("### form.journal_date.data:        ", form.journal_date.data)
#     print("### form.account_number.data:          ", form.account_number.data)
#     print("### form.department_number.data:       ", form.department_number.data)
#     print("### form.journal_entry_type.data:  ", form.journal_entry_type.data)
#     print("### form.journal_debit.data:      ", form.journal_debit.data)
#     print("### form.journal_credit.data:      ", form.journal_credit.data)
#     print("### form.journal_description:      ", form.journal_description.data)
#     print("### form.journal_reference.data:   ", form.journal_reference.data)
#     print("### form.gl_post_reference.data:   ", form.gl_post_reference.data)
#     # print("### form.journal_entity.data:   ", form.journal_entity.data)
#     # print("### form.journal_currency.data:   ", form.journal_currency.data)
#     print("### validate_on_submit:            ", form.validate_on_submit())
#     print("############################################################")

#     if form.validate_on_submit():

#         journal_entry = Journal(journal_name=form.journal_name.data,
#                                 journal_date=form.journal_date.data,
#                                 account_number=form.account_number.data,
#                                 department_number=form.department_number.data,
#                                 journal_entry_type=form.journal_entry_type.data,
#                                 journal_debit=form.journal_debit.data,
#                                 journal_credit=form.journal_credit.data,
#                                 journal_description=form.journal_description.data,
#                                 journal_reference=form.journal_reference.data,
#                                 journal_batch_id=batch_id,  #form.journal_batch_id.data,
#                                 gl_post_reference=form.gl_post_reference.data,
#                                 journal_entity=batch_entity, #form.journal_entity.data,
#                                 journal_currency=batch_currency, #form.journal_currency.data,
#                                 )

#         db.session.add(journal_entry)
#         db.session.commit()
#         flash("Journal Entry Created")
#         return redirect(url_for('core.index'))

#     return render_template('accounting/journal_entry.html', form=form, dept_list=dept_list, journal_batch_row_id=journal_batch_row_id, batch_id=batch_id, batch_entity=batch_entity, batch_currency=batch_currency, entity_name=entity_name, currency__=currency__, account_list=account_list,)

# ###############################################################################
# # TODO
# # REMOVE when ready
# # Keep this code for generic Journal Entry. It requires manual entry of the
# # entity and currency

# # @journals.route('/je_entry', methods=['GET', 'POST'])
# # # @login_required
# # def je_entry():
# #     form = JournalEntryForm()
# #     dept_list = Departments.query.all()

# #     # if form.validate_on_submit() is False:
# #     #     return render_template('accounting/acctg_message.html', form=form)

# #     #  TODO  check form data here
# #     print("############################################################")
# #     print("### form.errors:                   ", form.errors)
# #     print("### journal_name.data:             ", form.journal_name.data)
# #     print("### form.journal_date.data:        ", form.journal_date.data)
# #     print("### form.account_number.data:          ", form.account_number.data)
# #     print("### form.department_number.data:       ", form.department_number.data)
# #     print("### form.journal_entry_type.data:  ", form.journal_entry_type.data)
# #     print("### form.journal_debit.data:      ", form.journal_debit.data)
# #     print("### form.journal_credit.data:      ", form.journal_credit.data)
# #     print("### form.journal_description:      ", form.journal_description.data)
# #     print("### form.journal_reference.data:   ", form.journal_reference.data)
# #     print("### form.gl_post_reference.data:   ", form.gl_post_reference.data)
# #     print("### form.journal_entity.data:   ", form.journal_entity.data)
# #     print("### form.journal_currency.data:   ", form.journal_currency.data)
# #     print("### validate_on_submit:            ", form.validate_on_submit())
# #     print("############################################################")

# #     if form.validate_on_submit():

# #         journal_entry = Journal(journal_name=form.journal_name.data,
# #                                 journal_date=form.journal_date.data,
# #                                 account_number=form.account_number.data,
# #                                 department_number=form.department_number.data,
# #                                 journal_entry_type=form.journal_entry_type.data,
# #                                 journal_debit=form.journal_debit.data,
# #                                 journal_credit=form.journal_credit.data,
# #                                 journal_description=form.journal_description.data,
# #                                 journal_reference=form.journal_reference.data,
# #                                 journal_batch_id=form.journal_batch_id.data,
# #                                 gl_post_reference=form.gl_post_reference.data,
# #                                 journal_entity=form.journal_entity.data,
# #                                 journal_currency=form.journal_currency.data,
# #                                 )

# #         db.session.add(journal_entry)
# #         db.session.commit()
# #         flash("Journal Entry Created")
# #         return redirect(url_for('core.index'))

# #     # flash("CHECK IF JE WENT THROUGH")

# #     return render_template('accounting/journal_entry.html', form=form, dept_list=dept_list)

# ###############################################################################


# @journals.route('/create_batch', methods=['GET', 'POST'])
# # @login_required
# def create_batch():

#     """Route to create a new batch. Need to provide a batch ID (or a name), a
#     brief description, associated entity and currency.
#     """

#     form = BatchEntryForm()

#     entity_list = Entity.query.all()
#     currency_list = Currency.query.all()

#     # if form.validate_on_submit() is False:
#     #     return render_template('accounting/acctg_message.html', form=form)

#     #  TODO  check form data here
#     print("############################################################")
#     print("### form.errors:                      ", form.errors)
#     print("### journal_batch_id.data:            ", form.journal_batch_id.data)
#     print("### form.journal_batch_desc.data:     ", form.journal_batch_description.data)
#     print("### form.journal_batch_entity.data:   ", form.journal_batch_entity.data)
#     print("### form.journal_batch_currency.data: ", form.journal_batch_currency.data)
#     print("### form.gl_post_reference.data: ", form.gl_post_reference.data)
#     print("### validate_on_submit:            ", form.validate_on_submit())
#     print("############################################################")

#     if form.validate_on_submit():

#         create_batch = JournalBatch(journal_batch_id=form.journal_batch_id.data,
#                                     journal_batch_description=form.journal_batch_description.data,
#                                     journal_batch_entity=form.journal_batch_entity.data,
#                                     journal_batch_currency=form.journal_batch_currency.data,
#                                     gl_post_reference="NEED GL POST REF"
#                                     )

#         db.session.add(create_batch)
#         db.session.commit()
#         flash("Batch ID Created")
#         return redirect(url_for('journals.batch_list'))  # Need to redirect to

#     return render_template('accounting/create_batch.html', form=form,
#                            entity_list=entity_list,
#                            currency_list=currency_list,
#                            )

# ###############################################################################


# @journals.route('/batch_list', methods=['GET', 'POST'])
# # @login_required
# def batch_list():

#     """A list of the available batches. This list will exclude batches that
#     have already posted. Select a batch to start adding journal entries or to
#     review for posting to the GL.
#     """

#     batch_list = JournalBatch.query.filter(or_(JournalBatch.gl_batch_status == 0, JournalBatch.gl_batch_status == 1, JournalBatch.gl_batch_status == 2,))

#     return render_template('accounting/batch_list.html',
#                            batch_list=batch_list,
#                            )

# ###############################################################################


# @journals.route('/batch_list_posted', methods=['GET', 'POST'])
# # @login_required
# def batch_list_posted():

#     """A list of batches that have posted to the General Ledger.
#     """

#     batch_list_posted = JournalBatch.query.filter_by(gl_batch_status=3)

#     return render_template('accounting/batch_list_posted.html',
#                            batch_list_posted=batch_list_posted,
#                            )

# ###############################################################################


# @journals.route('/review_batch/<int:batch_row_id>', methods=['GET', 'POST'])
# # @login_required
# def review_batch(batch_row_id):

#     """Review JE's for a batch and mark ready to post to GL.
#     """

#     _batch = JournalBatch.query.filter_by(journal_batch_row_id=batch_row_id).first()

#     _batch_id = _batch.journal_batch_id

#     _batch_jes = Journal.query.filter_by(journal_batch_id=_batch.journal_batch_id)

#     # temp
#     print(f"*** TEMP *** batch_row_id arg : {batch_row_id}")

#     for je in _batch_jes:
#         print(f"*** TEMP *** _batch_jes : {je.journal_batch_id}")

#     _batch_gl_status = _batch.gl_batch_status

#     (batch_id__, total_DR, total_CR) = batch_total(_batch_id)
#     print("flag ***")

#     print("flag ORM +++++++++++++++++")

#     try:
#         orm_total_dr_qry = db.session.query(func.sum(Journal.journal_debit).label('tot_dr')).filter(Journal.journal_batch_id == _batch_id)

#         orm_total_cr_qry = db.session.query(func.sum(Journal.journal_credit).label('tot_cr')).filter(Journal.journal_batch_id == _batch_id)

#         print(f'+++ {(orm_total_dr_qry.first()[0] + 100000.0)}')

#         orm_total_dr = orm_total_dr_qry.first()[0]
#         orm_total_cr = orm_total_cr_qry.first()[0]

#         print(f'### DR: {orm_total_dr}')
#         print(f'### CR: {orm_total_cr}')
#     except TypeError:
#         print(f"ORM Totals > TypeError")
#         orm_total_dr = 999999999.0
#         orm_total_cr = 999999999.0

#         if _batch_gl_status == 0:
#             _batch_id = "No journal entries for "+ _batch.journal_batch_id + " data"

#         else:
#             _batch_id = "*** ERROR *** REVIEW "+ _batch.journal_batch_id + " data"

#     print("flag ORM +++++++++++++++++")

#     return render_template('accounting/batch_review.html',
#                            _batch_jes=_batch_jes,
#                            _batch_id=_batch_id,
#                            batch_id__=batch_id__,
#                            total_DR=total_DR,
#                            total_CR=total_CR,
#                            orm_total_dr=orm_total_dr,
#                            orm_total_cr=orm_total_cr,
#                            _batch_gl_status=_batch_gl_status,
#                            )

# ###############################################################################


# @journals.route('/load_batch/<int:batch_row_id>', methods=['GET', 'POST'])
# # @login_required
# def load_batch(batch_row_id):

#     """Select filename for journal entry csv file to be inserted into journals table. Files need to be saved in the je_csv_data folder within the web app root folder.
#     """

#     form = UploadFileForm()

#     if form.validate_on_submit():

#         filename = form.filename.data

#         load_file = batch_load_je_file(filename)

#         if load_file == "LOAD OK":
#             _batch = JournalBatch.query.filter_by(journal_batch_row_id=batch_row_id).first()

#             _batch_id = _batch.journal_batch_id

#             print(f"CHECK _batch_id: {_batch_id} <<<<<<<<<<<<<<<<<")

#             load_status = batch_load_insert(_batch_id)

#             if load_status == "INSERT COMPLETE":

#                 return redirect(url_for('journals.review_batch', batch_row_id=batch_row_id))
#             else:

#                 return render_template('accounting/load_error.html')

#     _batch = JournalBatch.query.filter_by(journal_batch_row_id=batch_row_id).first()

#     _batch_id = _batch.journal_batch_id

#     _batch_jes = Journal.query.filter_by(journal_batch_id=_batch.journal_batch_id)

#     (batch_id__, total_DR, total_CR) = batch_total(_batch_id)

#     return render_template('accounting/batch_load_file.html',
#                            form=form,
#                            _batch_jes=_batch_jes,
#                            _batch_id=_batch_id,
#                            batch_id__=batch_id__,
#                            total_DR=total_DR,
#                            total_CR=total_CR,
#                            )

# ###############################################################################


# @journals.route("/je_update/<batch_id>/<int:journal_id>", methods=['GET', 'POST'])
# # @login_required
# def je_update(batch_id, journal_id):

#     """Edit selected journal entry from batch review HTML and update.
#     """

#     _je = Journal.query.get_or_404(journal_id)

#     form = JournalUpdateForm()

#     if form.validate_on_submit():

#         _je.journal_name = form.journal_name.data
#         _je.journal_date = form.journal_date.data
#         _je.account_number = form.account_number.data
#         _je.department_number = form.department_number.data
#         _je.journal_entry_type = form.journal_entry_type.data
#         _je.journal_debit = form.journal_debit.data
#         _je.journal_credit = form.journal_credit.data
#         _je.journal_description = form.journal_description.data
#         _je.journal_reference = form.journal_reference.data
#         _je.journal_batch_id = form.journal_batch_id.data
#         _je.gl_post_reference = form.gl_post_reference.data
#         _je.journal_entity = form.journal_entity.data
#         _je.journal_currency = form.journal_currency.data

#         db.session.commit()
#         flash("JE Updated")

#         _batch_jes = Journal.query.filter_by(journal_batch_id=batch_id)
#         _batch_id = form.journal_batch_id.data
#         (batch_id__, total_DR, total_CR) = batch_total(_batch_id)

#         return render_template('accounting/batch_review.html',
#                                _batch_jes=_batch_jes,
#                                _batch_id=batch_id,
#                                total_DR=total_DR,
#                                total_CR=total_CR,
#                                orm_total_dr=0.0,  # For Update, making it zero
#                                orm_total_cr=0.0,  # For Update, making it zero
#                                )

#     elif request.method == 'GET':

#         form.journal_name.data = _je.journal_name
#         form.journal_date.data = _je.journal_date
#         form.account_number.data = _je.account_number
#         form.department_number.data = _je.department_number
#         form.journal_entry_type.data = _je.journal_entry_type
#         form.journal_debit.data = _je.journal_debit
#         form.journal_credit.data = _je.journal_credit
#         form.journal_description.data = _je.journal_description
#         form.journal_reference.data = _je.journal_reference
#         form.journal_batch_id.data = _je.journal_batch_id
#         form.gl_post_reference.data = _je.gl_post_reference
#         form.journal_entity.data = _je.journal_entity
#         form.journal_currency.data = _je.journal_currency

#     return render_template('/accounting/journal_entry_update.html',
#                            form=form,
#                            # entity_name=_je.journal_entity,
#                            # currency__=_je.journal_currency,
#                            )

# ###############################################################################


# @journals.route('/chart_of_accounts')
# def chart_of_accounts():

#     """Show list of accounts and various detail.
#     """

#     coa = ChartOfAccounts.query.all()

#     return render_template('accounting/chart_of_accounts.html',
#                            coa=coa,
#                            )

# ###############################################################################


# @journals.route('/general_ledger/<batch_id>', methods=['GET', 'POST'])
# def general_ledger(batch_id):

#     """Route for GL review of queries related to posting a batch of
#     journal entries to the general ledger.
#     """

#     print(f"TROUBLESHOOTING _ *********************************************")
#     print(f"TROUBLESHOOTING _ *********************************************")
#     # Get the batch DR/CR totals
#     (check_batch, check_DR, check_CR) = batch_total(batch_id)

#     print(f"CHECK ::::::::::: {check_batch}")
#     print(f"CHECK ::::::::::: {check_DR}")
#     print(f"CHECK ::::::::::: {check_CR}")

#     # Get the batch row id
#     batch_row_id = get_journal_batch_row_id(batch_id)
#     print(f"CHECK !!!!!!!!!!!!!!!!! {batch_row_id}")

#     count_check = Xref_Batch_GL_Staging.query.filter_by(batch_row_id=batch_row_id).count()

#     print(f"xref batch staging check: {count_check}")
#     print("")

#     # Get the batch row as an object from the batch_journal table
#     je_batch_id = JournalBatch.query.filter_by(journal_batch_row_id=batch_row_id).first()

#     if count_check == 0:

#         # batch_summary_gl aggregates the journal entries for the batch_id
#         # and inserts them into a gl staging table.
#         query_status, journals_summary_list = batch_summary_gl(batch_id)
#     else:
#         # Grab existing staged rows
#         query_status, journals_summary_list = get_staged_jes(batch_id)

#     for row_data in journals_summary_list:
#         print(f"journals_summary_list >>> {row_data}")

#     je_batch_stage = Journal.query.filter_by(journal_batch_id=je_batch_id.journal_batch_id)

#     gl_stage_status, gl_stage = batch_get_gl_staging(batch_id)

#     # REMOVE AFTER TESTING

#     for _ in gl_stage:

#         print(f"gl_stage row ++++++ {_}")

#     return render_template('accounting/general_ledger.html',
#                            je_batch_stage=je_batch_stage,
#                            check_batch=check_batch,
#                            check_DR=check_DR,
#                            check_CR=check_CR,
#                            query_status=query_status,
#                            journals_summary_list=journals_summary_list,
#                            gl_stage=gl_stage,
#                            batch_id=batch_id,
#                            )


# ###############################################################################


# @journals.route('/general_ledger_post/<batch_id>', methods=['GET', 'POST'])
# def general_ledger_post(batch_id):

#     """Process posting Batch ID provided to the General Ledger. The following steps will be completed:

#         - Rows from staging table will be inserted into the General Ledger table.
#         - Cross reference table (xref_batch_GL) will be updated to link the batch row id to the gl post reference.
#         - journal_batch.gl_batch_status field for batch id will be updated to three reflecting the completion of the batch to the GL.
#     """

#     ###########################################################################
#     # Delete after testing the code below

#     row_check = get_journal_batch_row_id(batch_id)

#     ###########################################################################

#     # Check if Batch_ID is already posted

#     journal_batch_row = JournalBatch.query.filter_by(journal_batch_id=batch_id).first()

#     print(f"*** general_ledger_post check: {journal_batch_row.journal_batch_id}")
#     if journal_batch_row.gl_batch_status == 3:

#         return render_template('accounting/general_ledger_posted_warning.html')

#     # Insert staging rows into General Ledger table
#     load_status = batch_staging_to_gl_insert(batch_id)

#     print(f"batch gl update status: {load_status}")

#     if load_status == "OK":

#         return render_template('accounting/general_ledger_post_successful.html',load_status=load_status, batch_id=batch_id, )

#     else:
#         return render_template('accounting/general_ledger_posted_warning_process_error.html')

# ###############################################################################


# @journals.route('/general_ledger_cancel_post/<batch_id>', methods=['GET', 'POST'])
# def general_ledger_cancel_post(batch_id):

#     """This route will cancel the GL posting process and remove the batch data from the staging table. The pending batches html will be rendered at the end of the process.
#     """

#     # Clear the staging table and reset the batch GL status to "2"

#     remove_status = clear_gl_staging(batch_id)

#     if remove_status == 'STAGING CLEAR - OK':

#         cancel_status = update_batch_gl_status(batch_id, 2)

#         if cancel_status == "OK":

#             return redirect(url_for('journals.batch_list'))

#         else:
#             return render_template('accounting/general_ledger_posted_warning_process_error.html')
#     elif remove_status == 'BATCH NOT STAGED':
#         # if batch has already been posted or is empty return to
#         # pending batches
#         return redirect(url_for('journals.batch_list'))

#     else:
#         return render_template('accounting/general_ledger_posted_warning_process_error.html')

# ###############################################################################


# @journals.route('/trialbalance', methods=['GET', 'POST'])
# def trialbalance():

#     """Prompt for accounting period to be passed to Trial Balance List"""

#     period_dropdown_list = db.session.query(Periods.period_description, Periods.period).order_by(Periods.period)

#     return render_template('accounting/trial_balance.html',
#                            period_dropdown_list=period_dropdown_list,
#                            )

# ###############################################################################


# @journals.route('/trialbalancelist/<int:period>', methods=['GET', 'POST'])
# def trialbalancelist(period):

#     """Display Trial Balance for a given period."""

#     period_dropdown_list = db.session.query(Periods.period_description, Periods.period).order_by(Periods.period)

#     period_description = db.session.query(Periods.period_description).filter_by(period=period).first()

#     trial_balance_list = gl_trial_balance(period)
#     return render_template('accounting/trial_balance_list.html',
#                            trial_balance_list=trial_balance_list,
#                            period_description=period_description[0],
#                            period_dropdown_list=period_dropdown_list,
#                            period=period,
#                            )
# ###############################################################################
# ###############################################################################
