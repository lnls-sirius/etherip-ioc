#!/bin/sh
set -x
set -e

SERVICE=rf-bo-interlock.service
cp ${SERVICE} /etc/systemd/system/${SERVICE}

systemctl daemon-reload
systemctl is-active --quiet ${SERVICE} && systemctl stop ${SERVICE}
systemctl enable ${SERVICE}
systemctl start  ${SERVICE}
