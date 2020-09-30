#!/bin/bash
pg_dump bitcoin > bitcoin.sql
gsutil cp bitcoin.sql gs://workflowkddc/Bitcoin/comments/gold