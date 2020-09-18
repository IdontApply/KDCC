from kubernetes.client import models as k8s

from airflow import DAG
from airflow.kubernetes.pod import Port
from airflow.kubernetes.secret import Secret
from airflow.kubernetes.volume import Volume
from airflow.kubernetes.volume_mount import VolumeMount
# from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
# from airflow.utils.dates import days_ago

with DAG(
    dag_id='example_kubernetes_operator',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    k = KubernetesPodOperator(
        namespace='default',
        image="ubuntu:16.04",
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "bar"},
        # secrets=[secret_file, secret_env, secret_all_keys],
        # ports=[port],
        # volumes=[volume],
        # volume_mounts=[volume_mount],
        name="airflow-test-pod",
        task_id="task",
        # affinity=affinity,
        # is_delete_operator_pod=True,
        # hostnetwork=False,
        # tolerations=tolerations,
        # configmaps=configmaps,
        # init_containers=[init_container],
        priority_class_name="medium",
    )

    # [START howto_operator_k8s_private_image]
    # quay_k8s = KubernetesPodOperator(
    #     namespace='default',
    #     image='quay.io/apache/bash',
    #     image_pull_secrets='testquay',
    #     cmds=["bash", "-cx"],
    #     arguments=["echo", "10", "echo pwd"],
    #     labels={"foo": "bar"},
    #     name="airflow-private-image-pod",
    #     is_delete_operator_pod=True,
    #     in_cluster=True,
    #     task_id="task-two",
    #     get_logs=True,
    # )
    # [END howto_operator_k8s_private_image]

    # [START howto_operator_k8s_write_xcom]
    # write_xcom = KubernetesPodOperator(
    #     namespace='default',
    #     image='alpine',
    #     cmds=["sh", "-c", "mkdir -p /airflow/xcom/;echo '[1,2,3,4]' > /airflow/xcom/return.json"],
    #     name="write-xcom",
    #     do_xcom_push=True,
    #     is_delete_operator_pod=True,
    #     in_cluster=True,
    #     task_id="write-xcom",
    #     get_logs=True,
    # )

    # pod_task_xcom_result = BashOperator(
    #     bash_command="echo \"{{ task_instance.xcom_pull('write-xcom')[0] }}\"",
    #     task_id="pod_task_xcom_result",
    # )
    # [END howto_operator_k8s_write_xcom]
k