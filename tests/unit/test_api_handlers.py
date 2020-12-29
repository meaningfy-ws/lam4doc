#!/usr/bin/python3

# sparql_adapter.py
# Date:  27/12/2020
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com

from lam4doc.entrypoints.api.handlers import upload_rdfs


def test_upload_rdfs_dataset_mandatory():
    result = upload_rdfs({}, None, None, None)
    assert result[0] == 'Dataset name is required'
    assert result[1] == 400


def test_upload_rdfs_at_least_one_file_mandatory():
    result = upload_rdfs({"dataset_name": "test"}, None, None, None)
    assert result[0] == "Please supply at least one file: lam_properties_document, lam_classes_document, " \
                        "celex_classes_document"
    assert result[1] == 400
