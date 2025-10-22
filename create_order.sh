#!/bin/bash

curl -X POST http://localhost:8000/orders \
	-H "Content-Type: application/json" \
	-d '{"customer":"John","product":"Book","amount":3}'


