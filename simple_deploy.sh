#!/bin/bash
echo "简单部署脚本"
docker-compose down 2>/dev/null
docker-compose up -d
echo "完成"
