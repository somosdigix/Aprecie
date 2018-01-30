docker run \
    -e "AZURE_APP_NAME=aprecieme" \
    -e "AZURE_APP_NAME=aprecieme" \
    -e "AZURE_DB_USERNAME=aprecieme" \
    -e "AZURE_DB_PASSWORD=G=wbFS8$Lx5pDp5-" \
    -e "AZURE_DB_HOST=aprecieme.database.windows.net" \
    -e "AZURE_DB_PORT=1433" \
    -it \
    --rm \
    -p 2222:8000 \
    renansmoreira/aprecieme:v1.0.0