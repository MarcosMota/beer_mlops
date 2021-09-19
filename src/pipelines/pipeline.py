import os

import boto3
import sagemaker

from sagemaker.inputs import TrainingInput

from sagemaker.processing import ProcessingInput, ProcessingOutput, ScriptProcessor

from sagemaker import Model
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.model_metrics import (
    MetricsSource,
    ModelMetrics,
)
from sagemaker.workflow.parameters import (
    ParameterInteger,
    ParameterString,
)
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, CacheConfig
from sagemaker.workflow.step_collections import RegisterModel, CreateModelStep

from sagemaker.inputs import CreateModelInput
from sagemaker.workflow.steps import CreateModelStep

from sagemaker.model_metrics import MetricsSource, ModelMetrics
from sagemaker.workflow.step_collections import RegisterModel

from pyathena import connect
import pandas as pd
from io import StringIO 

from sagemaker import image_uris

from sagemaker.inputs import TrainingInput
from sagemaker.workflow.steps import TrainingStep


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def get_sagemaker_client(region):
    """Gets the sagemaker client.

       Args:
           region: the aws region to start the session
           default_bucket: the bucket to use for storing the artifacts

       Returns:
           `sagemaker.session.Session instance
       """

    boto_session = boto3.Session(region_name=region)
    sagemaker_client = boto_session.client("sagemaker")
    return sagemaker_client


def get_session(region, default_bucket):
    """Gets the sagemaker session based on the region.

    Args:
        region: the aws region to start the session
        default_bucket: the bucket to use for storing the artifacts

    Returns:
        `sagemaker.session.Session instance
    """

    boto_session = boto3.Session(region_name=region)

    sagemaker_client = boto_session.client("sagemaker")
    runtime_client = boto_session.client("sagemaker-runtime")
    return sagemaker.session.Session(
        boto_session=boto_session,
        sagemaker_client=sagemaker_client,
        sagemaker_runtime_client=runtime_client,
        default_bucket=default_bucket,
    )


def get_pipeline_custom_tags(new_tags, region, sagemaker_project_arn=None):
    try:
        sm_client = get_sagemaker_client(region)
        response = sm_client.list_tags(
            ResourceArn=sagemaker_project_arn)
        project_tags = response["Tags"]
        for project_tag in project_tags:
            new_tags.append(project_tag)
    except Exception as e:
        print(f"Error getting project tags: {e}")
    return new_tags


def get_pipeline(
    role: str,
    region: str,
    s3_dataset: str,
    name: str = 'Beer'):
    

    default_bucket = sagemaker.session.Session().default_bucket()
    base_job_prefix = name.lower()
    sagemaker_session = get_session(region, default_bucket)
    if role is None:
        role = sagemaker.session.get_execution_role(sagemaker_session)

    processing_instance_count = ParameterInteger(name="ProcessingInstanceCount", default_value=1)
    processing_instance_type = ParameterString(
        name="ProcessingInstanceType", default_value="ml.m5.xlarge"
    )
    training_instance_type = ParameterString(name="TrainingInstanceType", default_value="ml.m5.xlarge")
    model_approval_status = ParameterString(
        name="ModelApprovalStatus", default_value="PendingManualApproval"
    )
    input_data = ParameterString(
        name="InputDataUrl",
        default_value=s3_dataset,
    )

    cache_config = CacheConfig(enable_caching=True, expire_after="30d")

    sklearn_processor = SKLearnProcessor(
        framework_version="0.23-1",
        instance_type=processing_instance_type,
        instance_count=processing_instance_count,
        base_job_name=f"{base_job_prefix}/script-preprocess",
        sagemaker_session=sagemaker_session,
        role=role,
    )
    step_process = ProcessingStep(
        name=f"Preprocess{name}Data",
        processor=sklearn_processor,
        inputs=[ProcessingInput(source=input_data, destination="/opt/ml/processing/input")],
        outputs=[
            ProcessingOutput(output_name="train", source="/opt/ml/processing/train"),
            ProcessingOutput(output_name="test", source="/opt/ml/processing/test"),
        ],
        code="src/pipelines/preprocessing.py",
        job_arguments=["--train-test-split-ratio", "0.2"],
        cache_config=cache_config,
    )



    model_path = f"s3://{default_bucket}/{name}Train"

    estimator = SKLearn(
        entry_point='training.py',
        framework_version='0.23-1',
        role=role,
        instance_count=1, 
        instance_type=training_instance_type,
        output_path=model_path,
        hyperparameters={
            'max_depth': 2,
            'n_estimators': 100,
            'random_state': 46
        }
    )


    step_train = TrainingStep(
        name="{name}Train",
        estimator=estimator,
        inputs={
            "train": TrainingInput(
                s3_data=step_process.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri,
                content_type="text/csv",
            )
        },
    )


    image_uri = image_uris.retrieve(
        framework="sklearn",
        region=region,
        version="0.23-1",
        py_version="py3",
        instance_type=processing_instance_type,
    )

    script_eval = ScriptProcessor(
        image_uri=image_uri,
        command=["python3"],
        instance_type=processing_instance_type,
        instance_count=1,
        base_job_name=f"{name}/scrpt-eval",
        role=role,
    )

    evaluation_report = PropertyFile(
        name="EvaluationReport", output_name="evaluation", path="evaluation.json"
    )
    step_eval = ProcessingStep(
        name=f"{name}Eval",
        processor=script_eval,
        inputs=[
            ProcessingInput(
                source=step_train.properties.ModelArtifacts.S3ModelArtifacts,
                destination="/opt/ml/processing/model",
            ),
            ProcessingInput(
                source=step_process.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri,
                destination="/opt/ml/processing/test",
            ),
        ],
        outputs=[
            ProcessingOutput(output_name="evaluation", source="/opt/ml/processing/evaluation"),
        ],
        code="src/pipelines/evaluate.py",
        property_files=[evaluation_report],
    )

    model = Model(
        image_uri=image_uri,
        model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
        sagemaker_session=sagemaker_session,
        role=role,
    )
    inputs = CreateModelInput(
        instance_type="ml.m5.large",
        accelerator_type="ml.eia1.medium",
    )
    step_create_model = CreateModelStep(
        name=f"{name}CreateModel",
        model=model,
        inputs=inputs,
    )


    model_metrics = ModelMetrics(
        model_statistics=MetricsSource(
            s3_uri="{}/evaluation.json".format(
                step_eval.arguments["ProcessingOutputConfig"]["Outputs"][0]["S3Output"]["S3Uri"]
            ),
            content_type="application/json",
        )
    )
    step_register = RegisterModel(
        name=f"{name}RegisterModel",
        estimator=estimator,
        model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
        content_types=["text/csv"],
        response_types=["text/csv"],
        inference_instances=["ml.t2.medium", "ml.m5.xlarge"],
        transform_instances=["ml.m5.xlarge"],
        model_package_group_name=f'{name}-package-group',
        approval_status=model_approval_status,
        model_metrics=model_metrics,
    )

    pipeline = Pipeline(
        name="{name}-pipeline",
        parameters=[
            processing_instance_type,
            processing_instance_count,
            training_instance_type,
            input_data,
            model_approval_status,
        ],
        steps=[step_process, step_train, step_eval, step_register, step_create_model],
        sagemaker_session=sagemaker_session,
    )

