#!/bin/bash
set -e

DOCKER_IMAGE_NAME="supervisely/main-import:0.0.2-test"

# Determine script and project root directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/..")"


# Set SDK version
SDK_VER=6.73.580


# Always use project root as build context, and correct relative paths
docker build \
	--no-cache \
	-f "$SCRIPT_DIR/Dockerfile.tmpl" \
	--build-arg tag_ref_name=$SDK_VER \
	--build-arg RUNTIME_BASE_IMAGE=base-py-sdk-hardened \
	--build-arg REQUIREMENTS_FILE=dev_requirements.txt \
	--label python_sdk_version=$SDK_VER \
	-t $DOCKER_IMAGE_NAME \
	"$PROJECT_ROOT"

# Ask for confirmation before pushing
read -p "Push image $DOCKER_IMAGE_NAME to registry? [y/N]: " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
	docker push $DOCKER_IMAGE_NAME
else
	echo "Push cancelled."
fi
