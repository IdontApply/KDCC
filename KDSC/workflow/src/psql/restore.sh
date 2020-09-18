gsutil cp gs://workflowkddc/Bitcoin/comments/gold/bitcoin.sql .
# confilect with already exisiting schema, FIX. (what works now: manually droping, createing then restoring)
psql -d bitcoin < bitcoin.sql