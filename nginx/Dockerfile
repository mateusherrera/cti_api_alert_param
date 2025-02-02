FROM nginx:latest

# Removendo o arquivo de configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/*

# Copiando o arquivo de configuração do Nginx
COPY nginx.conf /etc/nginx/conf.d/

# Expondo porta 80
EXPOSE 8877
