#!/bin/bash
set -e

export XDG_RUNTIME_DIR=/asc/kcachegrind-dbus
export $(dbus-launch)

exec "$@"
