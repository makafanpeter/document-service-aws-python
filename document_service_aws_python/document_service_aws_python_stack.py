from aws_cdk import (
    # Duration,
    Stack, aws_dynamodb, RemovalPolicy, aws_lambda,
    # aws_sqs as sqs,
    aws_s3 as s3,
)


from aws_cdk.aws_apigateway import (
    RestApi,
    LambdaIntegration,
    CfnAuthorizer,
    AuthorizationType,
    MockIntegration,
    PassthroughBehavior,
    IntegrationResponse,
    MethodResponse
)

from aws_cdk.aws_dynamodb import Attribute, AttributeType, BillingMode
from constructs import Construct


class DocumentServiceAwsPythonStack(Stack):
    DOCUMENT_TABLE_NAME = 'NewDocuments'
    PARTITION_KEY = 'id'
    CREATE_DOCUMENT_FUNCTION = 'CreateDocument'
    AWS_REGION = 'eu-west-1'
    API_GATEWAY_ID = 'DocumentManagerApiGateway'
    S3_BUCKET = "DocumentServiceAwsPython-peter"

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # create dynamo table
        dynamo_table = aws_dynamodb.Table(
            self,
            self.DOCUMENT_TABLE_NAME,
            table_name=self.DOCUMENT_TABLE_NAME,
            partition_key=
            {
                'name': self.PARTITION_KEY,
                'type': AttributeType.STRING,
            },
            billing_mode=BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        create_document = aws_lambda.Function(self, self.CREATE_DOCUMENT_FUNCTION,
                                              runtime=aws_lambda.Runtime.PYTHON_3_6,
                                              handler="main.handler",
                                              code=aws_lambda.Code.from_asset("./document_service_aws_python/lambdas"
                                                                              "/create_documents"),
                                              environment={
                                                  'DOCUMENT_TABLE_NAME': self.DOCUMENT_TABLE_NAME,
                                                  'REGION': self.AWS_REGION
                                              })

        create_document_integration = LambdaIntegration(
            create_document,
            proxy=True,
            integration_responses=[IntegrationResponse(
                status_code='200',
                response_parameters={
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )])

        dynamo_table.grant_read_write_data(create_document)

        api_gateway = RestApi(self, self.API_GATEWAY_ID, rest_api_name='Document Manager API')
        api_gateway_resource = api_gateway.root.add_resource('documents')

        api_gateway_resource.add_method("POST", create_document_integration, method_responses=[MethodResponse(
                status_code='200',
                response_parameters={
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            )])

        # Set up a bucket
        bucket = s3.Bucket(self, self.S3_BUCKET)

        bucket.grant_read_write(create_document)


