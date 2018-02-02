docker run \
    -e "AZURE_APP_NAME=aprecieme" \
    -e "AZURE_APP_NAME=aprecieme" \
    -e "AZURE_DB_USERNAME=aprecieme" \
    -e "AZURE_DB_PASSWORD=BK9td6L2RK7ZfWCZ" \
    -e "AZURE_DB_HOST=191.232.165.20" \
    -e "AZURE_DB_PORT=1433" \
    -it \
    --rm \
    -p 2222:8000 \
    renansmoreira/aprecieme:v1.0.0