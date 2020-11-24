{{- define "db-fullname" -}}
{{- $name := default .Chart.Name .Values.Db.Name -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "db-env" -}}
          env:
            - name: POSTGRES_DB
              valueFrom:
                secretKeyRef:
                  name: postgres-secret-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-secret-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret-config
                  key: POSTGRES_PASSWORD
{{- end }}

{{/*
Return the apiVersion of deployment.
*/}}
{{- define "deployment.apiVersion" -}}
{{- if semverCompare "<1.14-0" .Capabilities.KubeVersion.GitVersion -}}
{{- print "extensions/v1beta1" -}}
{{- else if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
{{- print "apps/v1" -}}
{{- end -}}
{{- end -}}

