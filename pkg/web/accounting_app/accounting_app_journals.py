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

from ... database.sql_queries.queries_read import (select_all,
                                                   select_batch_available,
                                                   select_entity_name_by_id,
                                                   select_batch_by_row_id,
                                                   batch_total,
                                                   select_je_by_row_id,
                                                   )

from ... database.sql_queries.queries_insert import (insert_new_batch_name,
                                                     insert_new_je_transaction,
                                                     batch_load_je_file,
                                                     batch_load_insert,
                                                     )

from ... database.sql_queries.queries_update import je_transaction_update


from . forms import (JournalEntryForm,
                     JournalUpdateForm,
                     BatchEntryForm,
                     UploadFileForm,
                     )

# Table names set up

journal_loader_table = 'journal_loader'   # JE batch load staging table
journal_batch_table = 'journal_batch'   # JE batch table
journal_table = 'journal'
entity_table = 'entity'   # Entity table

accounting_app_journals_bp = Blueprint('accounting_app_journals_bp',
                                       __name__,
                                       template_folder='templates',
                                       static_folder='static',
                                       static_url_path='accounting_app')


###############################################################################

@accounting_app_journals_bp.route('/journals/hello_there', methods=['GET', 'POST'])
def hello_there():
    return '<h1>Hello There!</h1>'


@accounting_app_journals_bp.route('/journals/journals_strobe', methods=['GET', 'POST'])
def journals_strobe():

    """Endpoint to reference while building the pages and functions related to
    journal entries.
    """
    marker = 'Test Value Alpha'

    return render_template('journals/journals_strobe.html',
                           marker=marker,
                           )


@accounting_app_journals_bp.route('/journals/load_batch/<int:batch_row_id>', methods=['GET', 'POST'])
def load_batch(batch_row_id):

    """Select filename for journal entry csv file to be inserted into journals table. Files need to be saved in the je_csv_data folder within the web app root folder.
    """

    form = UploadFileForm()

    if form.validate_on_submit():
        filename = form.filename.data

        # load CSV data into staging table (journal_loader)
        load_file = batch_load_je_file(filename, batch_row_id)

        if load_file == "LOAD OK":
            return redirect(url_for('accounting_app_journals_bp.journal_loader_batch_review', batch_row_id=batch_row_id))
        else:
            return render_template('accounting_app_journals_bp/load_error.html')

    print(f'>>>>> {select_batch_by_row_id(journal_batch_table, batch_row_id)}')

    journal_batch_row = select_batch_by_row_id(journal_batch_table, batch_row_id)

    (batch_row_id,
     batch_name,
     batch_description,
     batch_entity,
     batch_currency,
     gl_post_reference,
     gl_batch_status,
     ) = journal_batch_row[0]

    print(f'**** batch name: {batch_name} ****')

    return render_template('/journals/batch_load_file.html',
                           form=form,
                           batch_name=batch_name,
                           test_test='TEST'
                           )


@accounting_app_journals_bp.route('/journals/journal_loader_to_journal/<int:batch_row_id>', methods=['GET', 'POST'])
def journal_loader_to_journal(batch_row_id):

    """Move batch transaction data from journal loader to journal"""

    load_status = batch_load_insert(batch_row_id)

    if load_status == "journal_load to journal INSERT COMPLETE":

        return redirect(url_for('accounting_app_journals_bp.journal_loader_batch_review', batch_row_id=batch_row_id))
    else:
        return render_template('journals/journal_batch_load_error.html')
    # return '<h1>Journals - journal_loader to journal endpoint</h1>'


@accounting_app_journals_bp.route('/journals/journal_batch_load_error')
def journal_batch_load_error():

    """If Journal Entry csv load file errors out, return this route"""

    return render_template('journals/journal_batch_load_error.html')
    # return '<h1>Journals - LOAD ERROR endpoint</h1>'


@accounting_app_journals_bp.route('/journals/journal_loader_batch_review/<int:batch_row_id>', methods=['GET', 'POST'])
def journal_loader_batch_review(batch_row_id):

    """Review JE's loaded into staging table (journal_loader) and mark ready to load into journal table.
    """

    # Get row for corresponding batch_row_id
    journal_batch_row = select_batch_by_row_id(journal_batch_table, batch_row_id)
    print(f'journal_batch_row: {journal_batch_row}')

    # Get batch_name  for corresponding batch_row_id
    batch_name = journal_batch_row[0][1]

    # Get rows for corresponding batch_row_id in journal table
    batch_jes = select_batch_by_row_id(journal_loader_table, batch_row_id)

    print('+' * 50)
    for _ in batch_jes:
        print(f'{_}')
    print('+' * 50)
    # Get gl status for corresponding batch_row_id
    journal_batch_gl_status = journal_batch_row[0][6]

    print('=' * 50)
    print(f'journal_batch_gl_status: {journal_batch_gl_status}')
    print('=' * 50)

    (batch_row_id, total_DR, total_CR) = batch_total(journal_loader_table, batch_row_id)

    print('/' * 50)
    print(f'batch_row_id: {batch_row_id}')
    print(f'total_DR: {total_DR}')
    print(f'total_CR: {total_CR}')
    print('/' * 50)

    # Flag to indicate source of JE's:
    #  - "Staging" - journal_loader
    #  - "General Journal" - journal

    je_source = 'Staging'

    print(f'end of endpoint processing before return render_template')

    return render_template('journals/batch_review.html',
                           batch_jes=batch_jes,
                           batch_row_id=batch_row_id,
                           batch_name=batch_name,
                           total_DR=total_DR,
                           total_CR=total_CR,
                           batch_gl_status=journal_batch_gl_status,
                           je_source=je_source,
                           )


@accounting_app_journals_bp.route('/journals/create_batch', methods=['GET', 'POST'])
def create_batch():

    """Route to create a new batch. Need to provide a batch ID (or a name), a
    brief description, associated entity and currency.
    """

    form = BatchEntryForm()

    entity_list = select_all('entity')
    currency_list = select_all('currency')

    # if form.validate_on_submit() is False:
    #     return render_template('accounting/acctg_message.html', form=form)

    #  TODO  check form data here
    print("############################################################")
    print("### form.errors:                      ", form.errors)
    print("### journal_batch_name.data:            ", form.journal_batch_name.data)
    print("### form.journal_batch_desc.data:     ", form.journal_batch_description.data)
    print("### form.journal_batch_entity.data:   ", form.journal_batch_entity.data)
    print("### form.journal_batch_currency.data: ", form.journal_batch_currency.data)
    print("### validate_on_submit:            ", form.validate_on_submit())
    print("############################################################")

    if form.validate_on_submit():
        # Insert new batch data into journal_batch table

        insert_new_batch_name(form.journal_batch_name.data,
                              form.journal_batch_description.data,
                              str(form.journal_batch_entity.data),
                              str(form.journal_batch_currency.data),
                              "NEED GL POST REF",  # default for new batch
                              "0",  # default for new batch
                              )

        flash("Batch ID Created")
        return redirect(url_for('accounting_app_journals_bp.batch_list'))

    return render_template('journals/create_batch.html', form=form,
                           entity_list=entity_list,
                           currency_list=currency_list,
                           )


@accounting_app_journals_bp.route('journals/batch_list', methods=['GET', 'POST'])
# @login_required
def batch_list():

    """A list of the available batches. This list will exclude batches that
    have already posted. Select a batch to start adding journal entries or to
    review for posting to the GL.
    """

    batch_list = select_batch_available(journal_batch_table)

    print(f'{batch_list}')

    return render_template('journals/batch_list.html',
                           batch_list=batch_list,
                           )


@accounting_app_journals_bp.route('/je_entry/<int:journal_batch_row_id>', methods=['GET', 'POST'])
# @login_required
def je_entry(journal_batch_row_id):

    """Journal Entry route. After selecting a specific batch, the user is
    redirected to the Journal Entry page for the selected batch. Entity and
    currency are hardcoded to the JE. Assumption is that a batch will only
    be associated with a single entity and single currency.
    """

    form = JournalEntryForm()
    dept_list = select_all('departments')
    account_list = select_all('chart_of_accounts')

    batch_ = select_batch_by_id('journal_batch_table', journal_batch_row_id)

    batch_id = batch_[1]   # journal_batch_id
    batch_entity = batch_[3]   # journal_batch_entity
    batch_currency = batch_[4]   #journal_batch_currency
    entity_name = select_entity_name_by_id(entity_table, batch_entity)
    currency__ = select_all('currency')

    #  Check form data here
    print("############################################################")
    print("### journal_batch_row_id:              ", journal_batch_row_id)
    print("### batch_id:                      ", batch_id)
    print("### entity_name:                   ", entity_name)
    print("### currency:                   ", currency__[1])
    print("### currency description:                   ", currency__[2])
    print("### batch_entity:                  ", batch_entity)
    print("### batch_currency:                ", batch_currency)
    print("### form.errors:                   ", form.errors)
    print("### journal_name.data:             ", form.journal_name.data)
    print("### form.journal_date.data:        ", form.journal_date.data)
    print("### form.account_number.data:          ", form.account_number.data)
    print("### form.department_number.data:       ", form.department_number.data)
    print("### form.journal_entry_type.data:  ", form.journal_entry_type.data)
    print("### form.journal_debit.data:      ", form.journal_debit.data)
    print("### form.journal_credit.data:      ", form.journal_credit.data)
    print("### form.journal_description:      ", form.journal_description.data)
    print("### form.journal_reference.data:   ", form.journal_reference.data)
    print("### form.gl_post_reference.data:   ", form.gl_post_reference.data)
    print("### validate_on_submit:            ", form.validate_on_submit())
    print("############################################################")

    if form.validate_on_submit():

        insert_new_je_transaction(form.journal_name.data,
                                  form.journal_date.data,
                                  form.account_number.data,
                                  form.department_number.data,
                                  form.journal_entry_type.data,
                                  form.journal_debit.data,
                                  form.journal_credit.data,
                                  form.journal_description.data,
                                  form.journal_reference.data,
                                  batch_id,
                                  form.gl_post_reference.data,
                                  batch_entity,
                                  batch_currency,
                                  )

        flash("Journal Entry Created")
        return redirect(url_for('index'))

    return render_template('journals/journal_entry.html', form=form, dept_list=dept_list, journal_batch_row_id=journal_batch_row_id, batch_id=batch_id, batch_entity=batch_entity, batch_currency=batch_currency, entity_name=entity_name, currency__=currency__, account_list=account_list,)


@accounting_app_journals_bp.route("/journals/je_update/<int:batch_row_id>/<int:row_id>", methods=['GET', 'POST'])
# @login_required
def je_update(batch_row_id, row_id):

    """Edit selected journal entry from batch review HTML and update.
    """

    # Convert to SQL function for MariaDB
    _je = select_je_by_row_id(journal_loader_table, row_id)

    print(f'beginning of func _je_list: {_je}')

    # Check _je
    print('=' * 60)
    print(f'_je: {_je}')
    print('=' * 60)

    form = JournalUpdateForm()

    if form.validate_on_submit():

        _je_list = list(_je[0])

        _je_list[1] = form.journal_date.data
        _je_list[2] = form.account_number.data
        _je_list[3] = form.department_number.data
        _je_list[4] = form.journal_entry_type.data
        _je_list[5] = form.journal_debit.data
        _je_list[6] = form.journal_credit.data
        _je_list[7] = form.journal_description.data
        _je_list[8] = form.journal_reference.data
        _je_list[9] = form.journal_batch_row_id.data
        _je_list[10] = form.gl_post_reference.data
        _je_list[11] = form.journal_entity.data
        _je_list[12] = form.journal_currency.data

        je_transaction_update(_je_list)

        flash("*** JE Updated ***")

        # Get row for batch in journal_batch
        journal_batch_row = select_batch_by_row_id(journal_batch_table, batch_row_id)

        # Get batch_name  for corresponding batch_row_id
        batch_name = journal_batch_row[0][1]

        # Get rows for corresponding batch_row_id in journal table
        batch_jes = select_batch_by_row_id(journal_loader_table, batch_row_id)

        # Get gl status for corresponding batch_row_id
        journal_batch_gl_status = journal_batch_row[0][6]

        (batch_row_id, total_DR, total_CR) = batch_total(journal_loader_table, batch_row_id)

        return render_template('journals/batch_review.html',
                               batch_jes=batch_jes,
                               batch_row_id=batch_row_id,
                               batch_name=batch_name,
                               total_DR=total_DR,
                               total_CR=total_CR,
                               batch_gl_status=journal_batch_gl_status,
                               )

    elif request.method == 'GET':
        # print(f'_je: {_je}')
        # print(f'_je[1]: {_je[0]}')
        # print(f'_je[2]: {_je[0]}')
        # print(f'_je[0][1]: {_je[0][]}')
        form.journal_date.data = _je[0][1]
        form.account_number.data = _je[0][2]
        form.department_number.data = _je[0][3]
        form.journal_entry_type.data = _je[0][4]
        form.journal_debit.data = _je[0][5]
        form.journal_credit.data = _je[0][6]
        form.journal_description.data = _je[0][7]
        form.journal_reference.data = _je[0][8]
        form.journal_batch_row_id.data = _je[0][9]
        form.gl_post_reference.data = _je[0][10]
        form.journal_entity.data = _je[0][11]
        form.journal_currency.data = _je[0][12]

    return render_template('/journals/journal_entry_update.html',
                           form=form,
                           # entity_name=_je.journal_entity,
                           # currency__=_je.journal_currency,
                           )


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
