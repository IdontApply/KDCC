# KDSC
# Kubernetes data science cluster

KDSC is a cloud data pipeline implementation using the following tools:
- Terraform: for setting up infrastructure <br>
- GKE: a manged implementation of Kubernetes, where the workflow will run  <br>
- argo: data workflow, where each workflow-step is a Kubernetes pod  <br>
- docker: container run time. <br>
- python: workflow execution code. <br>
- postgres: RDBM. <br>
- GCS: googles implementation of object storage. <br>
- minio: container native object storage. <br>
- s3: aws implementation of object storage. <br>
-  skaffold (optional). <br>
### fill in prerequisites
- gloud, gcloud authenticated and ready.
- aws shared credentials file in $HOME/.aws/credentials.
- Terrafrom variables.<br>
note: prerequisites will be annotated by (*)
### infrastructure(Terrafrom)
infrastructure is split into 2 parts gcp resources and aws resources:
- gcp:([*]())
  - GKE cluster
  - GCS google cloud storage
- aws:([*]())
  - s3 
### structure(KDSC)
- kubernetes-kubectl
  - aws.secrets.yaml > credentials, key_id and access_key.([*]())
  - postgres.secrets.yaml > postgres credential
- kubernetes-manifests
  - postgres deployment.
  - psql deployment: used for debugging and querying the db.
- src(docker images):
  - bitcoin: used for bitcoin workflow.
  - getter: data getter tools. used for bitcoin workflow.
  - postgres: used in the postgres deployment.(note: bitcoin database schema located here)
  - psql: used by psql deployment.
  - python: used in germanen workflow.
  - jupyter-viola: used in germanen workflow.
- workflow(argo):
  - bitcoin:
    - bitcoin-comment-getter.yaml
    - bitcoin-comment-porcess.yaml
    - bitcoin-post.yaml
  - germanen:
    - germanen.yaml
    - germanen-store-s3.yaml