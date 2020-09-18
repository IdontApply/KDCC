#!/bin/bash

# set up the GKE and s3 using terrafrom

cd ./terraform/gcp
sudo terraform apply
POST https://iam.googleapis.com/v1/projects/$project_id/serviceAccounts/storage-user@$project_id.iam.gserviceaccount.com/keys

terraform output
kubernetes_cluster_name=$(terraform output -json kubernetes_cluster_name | jq '.' -r | less)
zone=$(terraform output -json zone | jq '.' -r | less)
project_id=$(terraform output -json project_id | jq '.' -r | less)

gcloud container clusters get-credentials $kubernetes_cluster_name --zone $zone
cd ../..
cd ./terraform/aws
sudo terraform apply
cd ../..

# # set up argo namespace and secterts(note: )
kubectl create ns argo
kubectl apply -f ./workflow/kubernetes-kubectl

# # set up argo
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/quick-start-postgres.yaml
# # set up minio as argo-artifacts
helm install argo-artifacts stable/minio --set service.type=LoadBalancer --set fullnameOverride=argo-artifacts -n argo

# # build images for the workflows, using docker build and push. Or use skaffold with a one liner, if so comment the docker lines.
# skaffold dev -v info --port-forward --rpc-http-port 33221 --filename skaffold.yaml --default-repo gcr.io/$project_id
cd workflow/src
docker build bitcoin/. -t  gcr.io/$project_id/bitcoin-worker
docker push  gcr.io/$project_id/bitcoin-worker

docker build postgres/. -t  gcr.io/$project_id/postgres-worker
docker push  gcr.io/$project_id/postgres-worker

docker build getter/. -t  gcr.io/$project_id/getter-worker
docker push  gcr.io/$project_id/getter-worker

docker build jupyter-viola/. -t  gcr.io/$project_id/jupyter-viola-worker
docker push  gcr.io/$project_id/jupyter-viola-worker

docker build python/. -t  gcr.io/$project_id/python-worker
docker push  gcr.io/$project_id/python-worker

cd ../..

cd KDSC/workflow
# submit bitcoing getter to donwnload and parse reddit comments, for only Bitcoin subbreddit. best way to run it is year by year 
argo submit -n argo --watch bitcoin-comment-getter.yaml # note this is set up for one year data, not be taxing on the website hosting the data
# argo submit -n argo --watch bitcoin-comment-getter-missing.yaml
argo submit -n argo --watch bitcoin-price-getter.yaml
argo submit -n argo --watch bitcoin-process.yaml
argo submit -n argo --watch bitcoin-post.yaml

# submit germen power plants workflow
argo submit -n argo --watch germanen.yaml


cd ../..

# destroy infstrucure 
cd ./terraform/gke
sudo terraform destroy

# gsutil iam ch allUsers:objectViewer gs://BUCKET-NAME
# ^ for imagepull error

