#!/usr/bin/python3

# forms.py
# Date:  03/11/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com 

"""
Form classes for use in views.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import RadioField, StringField
from wtforms.validators import DataRequired

from lam4doc.config import HTML_REPORT_TYPE, PDF_REPORT_TYPE


class ReportTypeForm(FlaskForm):
    report_extension = RadioField('Choose the report extension',
                                  choices=[(HTML_REPORT_TYPE, 'HTML report'), (PDF_REPORT_TYPE, 'PDF report')])


class UploadRDFFilesForm(FlaskForm):
    dataset_name = StringField('Dataset name', validators=[DataRequired()])
    lam_properties_document = FileField('LAM properties document')
    lam_classes_document = FileField('LAM classes document')
    celex_classes_document = FileField('CELEX classes document')
