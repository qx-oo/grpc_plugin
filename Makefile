stub:
	python -m grpc_tools.protoc -I ./ --python_out=./ \
	--grpc_python_out=./ ./grpc_plugin/proto/*.proto
