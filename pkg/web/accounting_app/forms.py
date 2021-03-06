# forms.py

"""Forms for accounting system web app"""

from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SubmitField,
                     TextAreaField,
                     DateTimeField,
                     IntegerField,
                     FloatField,
                     SelectField,
                     DateField,
                     FileField,
                     )

from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired

from ... database.sql_queries.queries_read import select_all
# Get available rows from chart of accounts and departments tables to populate
# a list
chart_of_accounts_tbl = select_all('chart_of_accounts')
departments_tbl = select_all('departments')

acct_ = [(x[1], (str(x[1]) + " - " + x[2])) for x in chart_of_accounts_tbl]

dept_ = [(x[1], x[2]) for x in departments_tbl]

# comment out above code and use empty lists below when rebuilding database
# acct_ = []
# dept_ = []


class BatchEntryForm(FlaskForm):
    """Form to create a new Journal Entry Batch."""
    journal_batch_name = StringField('Batch Name', validators=[DataRequired()])
    journal_batch_description = StringField('Batch Description', validators=[DataRequired()])
    journal_batch_entity = SelectField(u'Entity', choices=[('1', 'North America - USD'), ('2', 'UK - GBP'), ('3', 'Germany - EUR'), ('4', 'France - EUR')])
    # journal_batch_entity = IntegerField('Entity', validators=[InputRequired()])
    # journal_batch_currency = IntegerField('Currency', validators=[InputRequired()])

    enter = SubmitField('Create Batch')


class JournalEntryForm(FlaskForm):
    """Form to create a new Journal Entry for a provided batch_id."""
    journal_name = StringField('Journal Name', validators=[DataRequired()])
    journal_date = DateField('Journal Date', validators=[DataRequired()])
    account_number = SelectField('Account Number', choices=acct_, coerce=int, validators=[DataRequired()])
    department_number = SelectField('Department Number', choices=dept_, coerce=int, validators=[DataRequired()])
    journal_entry_type = IntegerField('Type', validators=[DataRequired()])
    journal_debit = FloatField('Debit', validators=[InputRequired()])
    journal_credit = FloatField('Credit', validators=[InputRequired()])
    journal_description = StringField('Description', validators=[DataRequired()])
    journal_reference = StringField('Reference', validators=[DataRequired()])
    gl_post_reference = StringField('GL_Post_Reference', validators=[DataRequired()])
    enter = SubmitField('Enter')


class UploadFileForm(FlaskForm):
    filename = FileField('Choose Journal Entries file to open (must be csv format)', validators=[DataRequired()])

    enter = SubmitField('Load File')


class JournalUpdateForm(FlaskForm):

    journal_date = StringField('Journal Date (YYYY-MM-DD)', validators=[DataRequired()])
    account_number = SelectField('Account Number', choices=acct_, coerce=int, validators=[DataRequired()])
    department_number = SelectField('Department Number', choices=dept_, coerce=int, validators=[DataRequired()])
    journal_entry_type = IntegerField('Type', validators=[DataRequired()])
    journal_debit = FloatField('Debit', validators=[InputRequired()])
    journal_credit = FloatField('Credit', validators=[InputRequired()])
    journal_description = StringField('Description', validators=[DataRequired()])
    journal_reference = StringField('Reference', validators=[DataRequired()])
    journal_batch_row_id = IntegerField('JE_Batch_Row_ID', validators=[DataRequired()])
    gl_post_reference = StringField('GL_Post_Reference', validators=[DataRequired()])

    journal_entity = IntegerField('JE_entity', validators=[InputRequired()])
    journal_currency = IntegerField('JE_currency', validators=[DataRequired()])

    enter = SubmitField('Update')
