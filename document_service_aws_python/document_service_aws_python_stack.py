from aws_cdk import (
    # Duration,
    Stack, aws_dynamodb, RemovalPolicy, aws_lambda,
    # aws_sqs as sqs,
)
from aws_cdk.aws_apigateway import RestApi
from aws_cdk.aws_dynamodb import Attribute, AttributeType, BillingMode
from constructs import Construct


class DocumentServiceAwsPythonStack(Stack):
    DOCUMENT_TABLE_NAME = 'Documents'
    PARTITION_KEY = 'id'
    CREATE_DOCUMENT_FUNCTION = ''
    AWS_REGION = 'us-west-2'

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # create dynamo table
        dynamo_table = aws_dynamodb.Table(
            table_name=self.DOCUMENT_TABLE_NAME, partition_key=Attribute({
                'name': self.PARTITION_KEY, 'type': AttributeType.String,
            }), billing_mode=BillingMode.PayPerRequest, removal_policy=RemovalPolicy.DESTROY
        )

        create_document = aws_lambda.Function(self, self.CREATE_DOCUMENT_FUNCTION,
                                              runtime=aws_lambda.Runtime.PYTHON_3_6,
                                              handler="main.handler",
                                              code=aws_lambda.Code.from_asset("./lambdas/create_documents"),
                                              environment={
                                                  'DOCUMENT_TABLE_NAME': self.DOCUMENT_TABLE_NAME,
                                                  'AWS_REGION': self.AWS_REGION
                                               })

        dynamo_table.grant_read_write_data(create_document)

        api_gateway = RestApi(self, self.ID, rest_api_name='Document Manager API')
        api_gateway_resource = api_gateway.root.add_resource('documents')
        api_gateway_resource.add_method("POST",  create_document)



