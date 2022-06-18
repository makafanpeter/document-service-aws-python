import aws_cdk as core
import aws_cdk.assertions as assertions

from document_service_aws_python.document_service_aws_python_stack import DocumentServiceAwsPythonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in document_service_aws_python/document_service_aws_python_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DocumentServiceAwsPythonStack(app, "document-service-aws-python")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
