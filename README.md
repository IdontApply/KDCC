# KDSC
# Kubernetes data science cluster

A Helm chart for a simple Kubernetes data science cluater using the following tools:
- argo
- Spark
- Zippline
- postgres

charts used to build KDSC:
- argo: External  spark chart > https://github.com/argoproj/argo-helm/tree/master/charts/argo
- spark: External  spark chart > https://github.com/helm/charts/tree/master/stable/spark
- db: simple postgres dpeloyment for testing > https://github.com/IdontApply/KDSC/tree/master/kdsc/charts/db
