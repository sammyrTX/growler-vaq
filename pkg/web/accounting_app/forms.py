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


class BatchEntryForm(FlaskForm):
    journal_batch_id = StringField('Batch ID', validators=[DataRequired()])
    journal_batch_description = StringField('Batch Description', validators=[DataRequired()])
    journal_batch_entity = IntegerField('Entity', validators=[InputRequired()])
    journal_batch_currency = IntegerField('Currency', validators=[InputRequired()])
    gl_post_reference = StringField('GL_Post_Reference', validators=[DataRequired()])

    enter = SubmitField('Create Batch')
