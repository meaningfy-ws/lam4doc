# #!/usr/bin/python3
#
# # sparql_adapter.py
# # Date:  27/12/2020
# # Author: Laurentiu Mandru
# # Email: mclaurentiu79@gmail.com
# import pytest
# from werkzeug.exceptions import BadRequest, UnprocessableEntity
#
# from lam4doc.entrypoints.api.handlers import upload_rdfs, generate_lam_report
#
#
# def test_upload_rdfs_at_least_one_file_mandatory():
#     with pytest.raises(BadRequest) as http_error:
#         _ = upload_rdfs({"dataset_name": "test"}, None, None, None)
#
#     assert http_error.value.code == 400
#     assert 'Please supply at least one file: lam_properties_document, lam_classes_document, celex_classes_document' \
#            in http_error.value.description
#
#
# def test_generate_lam_report_exception_not_supported():
#     with pytest.raises(UnprocessableEntity) as http_error:
#         _ = generate_lam_report('jpeg')
#
#     assert http_error.value.code == 422
#     assert 'Wrong report_extension format. Accepted formats: html, pdf' in http_error.value.description
