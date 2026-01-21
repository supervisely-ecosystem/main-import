IMAGE_TAG="supervisely/autoimport_dev:0.0.1"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

docker build \
	-f "$ROOT_DIR/docker/Dockerfile" \
	-t "$IMAGE_TAG" \
	"$ROOT_DIR"

docker push "$IMAGE_TAG"