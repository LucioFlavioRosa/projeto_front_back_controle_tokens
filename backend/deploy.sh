#!/bin/bash

# Variáveis de ambiente necessárias
RESOURCE_GROUP="<SEU_RESOURCE_GROUP>"
APP_SERVICE_NAME="<SEU_APP_SERVICE_NAME>"
LOCATION="<SEU_LOCATION>"

# Build do projeto (ajuste conforme sua estrutura de build)
echo "Instalando dependências..."
pip install -r requirements.txt

# Login no Azure (caso necessário)
echo "Fazendo login no Azure..."
az login

# Configurar variáveis de ambiente (exemplo)
echo "Configurando variáveis de ambiente no App Service..."
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_SERVICE_NAME --settings APPINSIGHTS_CONNECTION_STRING="<SUA_CONNECTION_STRING>"

# Deploy do código para o Azure App Service
echo "Realizando deploy para o Azure App Service..."
az webapp up --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP --location $LOCATION --sku F1

echo "Deploy concluído."
