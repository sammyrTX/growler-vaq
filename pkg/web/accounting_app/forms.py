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

acct_ = [(x.account_number, (str(x.account_number) + " - " + x.account_name)) for x in chart_of_accounts_tbl]

dept_ = [(x.department_number, x.department_name) for x in departments_tbl]

# comment out above code and use empty lists below when rebuilding database
# acct_ = []
# dept_ = []


class BatchEntryForm(FlaskForm):
    """Form to create a new Journal Entry Batch."""
    journal_batch_id = StringField('Batch ID', validators=[DataRequired()])
    journal_batch_description = StringField('Batch Description', validators=[DataRequired()])
    journal_batch_entity = IntegerField('Entity', validators=[InputRequired()])
    journal_batch_currency = IntegerField('Currency', validators=[InputRequired()])
    gl_post_reference = StringField('GL_Post_Reference', validators=[DataRequired()])

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
