version=1.2.0
registry=gitlab.cs.pub.ro:5050/asc/asc-public
img_name=c-labs
tag_name=${registry}/${img_name}:${version}
#tag_name=test-asc:${img_name}-${version}

build:
	docker image build -t ${tag_name} --build-arg VERSION=${version} .

test: build
	docker run --rm --name ${img_name} ${tag_name}

run: build
	docker run -it --name ${img_name} -e QT_DEBUG_PLUGINS=1 ${tag_name} /bin/bash

bash:
	docker exec -it ${img_name} /bin/bash

push:
	docker login
	docker push ${tag_name}

clean:
	docker rm -f ${img_name}
	docker image rm ${tag_name}
