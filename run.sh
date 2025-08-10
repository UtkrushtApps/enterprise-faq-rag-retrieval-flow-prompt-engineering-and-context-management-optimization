#!/usr/bin/env bash
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
function check_docker {
  if ! docker info &>/dev/null; then
    echo -e "${RED}[ERROR] Docker daemon is not running.${NC}"
    exit 1
  fi
}
function cleanup {
  echo -e "${GREEN}Cleaning up containers and volumes...${NC}"
  docker-compose down -v || true
  docker system prune -f || true
}
function start_chroma_db {
  echo -e "${GREEN}Building and starting Chroma DB...${NC}"
  docker-compose up -d --build
  for i in {1..30}; do
    if docker exec chroma_faq_db curl -sf http://localhost:8000/_health > /dev/null; then
      echo -e "${GREEN}Chroma DB is running.${NC}"
      return 0
    fi
    sleep 2
  done
  echo -e "${RED}[ERROR] Timed out waiting for Chroma container health.${NC}"
  exit 2
}
function process_documents {
  echo -e "${GREEN}Processing FAQ documents and generating embeddings...${NC}"
  docker exec chroma_faq_db python3 /app/scripts/process_documents.py
}
function verify_setup {
  echo -e "${GREEN}Verifying database and setup...${NC}"
  docker exec chroma_faq_db python3 /app/scripts/verify_setup.py
}
echo -e "${GREEN}== [AUTOMATED RAG ENVIRONMENT SETUP START] ==${NC}"
check_docker
cleanup
start_chroma_db
process_documents
verify_setup
echo -e "${GREEN}== [SETUP COMPLETE: Ready for pipeline implementation] ==${NC}"
