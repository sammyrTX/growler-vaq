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
                                                   select_batch_loaded,
                                                   # select_entity_name_by_id,
                                                   select_batch_by_row_id,
                                                   batch_total,
                                                   # select_je_by_row_id,
                                                   select_rowcount_row_id,
                                                   # select_entity_list,
                                                   )

from ... database.sql_queries.queries_insert import (insert_new_batch_name,
                                                     insert_new_je_transaction,
                                                     batch_load_je_file,
                                                     batch_load_insert,
                                                     )

from ... database.sql_queries.queries_update import je_transaction_update

from ... database.sql_queries.queries_delete import delete_journal_batch

from . forms import (JournalEntryForm,
                     JournalUpdateForm,
                     BatchEntryForm,
                     UploadFileForm,
                     )

# Table names set up

journal_loader_table = 'journal_loader'   # JE batch load staging table
journal_batch_table = 'journal_batch'   # JE batch table
journal_table = 'journal'   # Journal table
entity_table = 'entity'   # Entity table

# Empty journal_loader result set
batch_jes_empty = ([0, 'NODATE', 0, 0, 0,  0.0, 0.0, 'NO DATA', '*******************', 0, '********', 0, 0])

accounting_app_journals_bp = Blueprint('accounting_app_journals_bp',
                                       __name__,
                                       template_folder='templates',
                                       static_folder='static',
                                       static_url_path='accounting_app')


###############################################################################

@accounting_app_journals_bp.route('/journals/hello_there', methods=['GET', 'POST'])
def hello_there():
    """Test route"""
    return '<h1>Hello There!</h1>'


@accounting_app_journals_bp.route('/journals/journals_strobe', methods=['GET', 'POST'])
def journals_strobe():
    """Test route - Endpoint to reference while building the pages and functions related to journal entries.
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

        if load_file == "LOAD OKAY":
            return redirect(url_for('accounting_app_journals_bp.journal_loader_batch_review', batch_row_id=batch_row_id))
        else:
            return render_template('accounting_app_journals_bp/load_error.html')

    journal_batch_row = select_batch_by_row_id(journal_batch_table, batch_row_id)

    (batch_row_id,
     batch_name,
     batch_description,
     batch_entity,
     batch_currency,
     gl_post_reference,
     gl_batch_status,
     ) = journal_batch_row[0]

    return render_template('/journals/batch_load_file.html',
                           form=form,
                           batch_name=batch_name,
                           test_test='TEST'
                           )


@accounting_app_journals_bp.route('/journals/journal_loader_to_journal/<int:batch_row_id>', methods=['GET', 'POST'])
def journal_loader_to_journal(batch_row_id):

    """Move batch transaction data from journal loader to journal"""

    load_status = batch_load_insert(batch_row_id)

    if load_status == 0:
        return redirect(url_for('accounting_app_journals_bp.journal_loader_batch_review', batch_row_id=batch_row_id))
    else:
        return render_template('journals/journal_batch_load_error.html')


@accounting_app_journals_bp.route('/journals/journal_batch_load_error')
def journal_batch_load_error():
    """If Journal Entry csv load file errors out, return this route"""
    return render_template('journals/journal_batch_load_error.html')


@accounting_app_journals_bp.route('/journals/journal_loader_batch_review/<int:batch_row_id>', methods=['GET', 'POST'])
def journal_loader_batch_review(batch_row_id):

    """Review JE's loaded into staging table (journal_loader) and mark ready to load into journal table.
    """

    # Get row for corresponding batch_row_id
    journal_batch_row = select_batch_by_row_id(journal_batch_table, batch_row_id)

    # Get batch_name for corresponding batch_row_id
    batch_name = journal_batch_row[0][1]

    # Check if the gl_batch_status is zero which indicates it is new with no
    # data loaded or if there are no corresponding rows in journal_loader
    # table indicating no csv file has been loaded to the staging table.

    if journal_batch_row[0][6] == 0 or select_rowcount_row_id(journal_loader_table, batch_row_id) == 0:

        # Set to a 'no rows' status
        je_source = 'New batch'
        journal_batch_gl_status = 0

        return render_template('journals/batch_review.html',
                               batch_jes=batch_jes_empty,
                               batch_row_id=batch_row_id,
                               batch_name=batch_name,
                               total_DR=0.0,
                               total_CR=0.0,
                               batch_gl_status=journal_batch_gl_status,
                               je_source=je_source,
                               )

    # Get rows for corresponding batch_row_id in journal table
    batch_jes = select_batch_by_row_id(journal_loader_table, batch_row_id)

    # Get gl status for corresponding batch_row_id
    journal_batch_gl_status = journal_batch_row[0][6]

    # Get total of Debits & Credits for batch_row_id
    (batch_row_id, total_DR, total_CR) = batch_total(journal_loader_table, batch_row_id)

    # Flag to indicate source of JE's:
    #  - "Staging" - journal_loader
    #  - "General Journal" - journal

    if journal_batch_gl_status == 10:
        je_source = 'Staging'
    elif journal_batch_gl_status == 20:
        je_source = 'Transactions Loaded'
    else:
        je_source = '*****'

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

    entity_list = [(1, 'North America', 1, 'USD'),  # Use this list for now
                   (2, 'UK - London', 2, 'GBP'),
                   ]

    # Call to deactivated function that retrieves entity info and currency code
    # May be able to remove if not needed in future versions.
    # entity_list = select_entity_list()

    if form.validate_on_submit():
        # Insert new batch data into journal_batch table

        insert_new_batch_name(form.journal_batch_name.data,
                              form.journal_batch_description.data,
                              str(form.journal_batch_entity.data),
                              '0', # str(form.journal_batch_currency.data),
                              "NEED GL POST REF",  # default for new batch
                              "0",  # default for new batch
                              )

        flash("Batch ID Created")
        return redirect(url_for('accounting_app_journals_bp.batch_list'))

    return render_template('journals/create_batch.html', form=form,
                           entity_list=entity_list,
                           )


@accounting_app_journals_bp.route('journals/batch_list', methods=['GET', 'POST'])
def batch_list():

    """A list of the available and loaded batches. Select a new batch to start adding journal entries or to review for posting to the GL.
    """

    batch_list = select_batch_available(journal_batch_table)
    batch_list_loaded = select_batch_loaded(journal_batch_table)

    return render_template('journals/batch_list.html',
                           batch_list=batch_list,
                           batch_list_loaded=batch_list_loaded,
                           )


@accounting_app_journals_bp.route('journals/batch_delete/<int:journal_batch_row_id>', methods=['GET', 'POST'])
def batch_delete(journal_batch_row_id):

    """Delete a batch that has not been loaded to the journal table.
    """

    delete_message = delete_journal_batch(journal_batch_row_id)

    return render_template('journals/batch_deleted.html',
                           journal_batch_row_id=journal_batch_row_id,
                           delete_message=delete_message,
                           )
