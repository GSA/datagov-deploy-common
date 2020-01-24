#!/bin/bash
# Data.gov Audit report
#
# Parse logs to summarize events, raise any issues that might need further
# investigation.

set -o errexit
set -o pipefail
set -o nounset

logwatch_detail=9
codename=$(lsb_release --codename --short)

function is_trusty () {
  [ "$codename" = "trusty" ]
}

function run_aureport () {
  /sbin/aureport --input-logs --start week-ago --interpret --summary "$@"
}

cat <<EOF
Hello Data.gov,

This is an audit report for control AU-6. Please review this log for any
anomalies. If you see something suspicious, please follow the Incident Response
Plan[1].

After reviewing this report, please update the audit log[2].


[1]: https://docs.google.com/document/d/1kb5cw1gD6VvfBhaH3BA67M2bEMivng44/edit
[2]: https://docs.google.com/spreadsheets/d/1z6lqmyNxC7s5MiTt9f6vT41IS2DLLJl4HwEqXvvft40/edit#gid=0


* * *
EOF

# Summary
run_aureport

# Command summary
# Trusty does not support --comm
is_trusty || run_aureport --comm

# Events summary
run_aureport --event

# Login summary
run_aureport --login

# Account modifications
# Trusty has not implemented the mods summary
is_trusty || run_aureport --mods

# Mandatory Access Control summary
run_aureport --mac

# Anomaly report
run_aureport --anomaly

# Executable report
run_aureport --executable

echo

# Include the logwatch report
/usr/sbin/logwatch --detail "$logwatch_detail" --range "between -7 days and -1 days" --output stdout \
  --service All \
  --service -zz-network \
  --service -zz-sys

# Print footer
cat <<EOF


--
$(basename $0) on $(hostname)
https://github.com/GSA/datagov-deploy-common
EOF
