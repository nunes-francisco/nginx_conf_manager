### # NGINX_CONF_MABAGER

![](assets/nginx_conf.png)

### Construindo e executando o container

``docker-compose up --build``

Vendo os logs:

``docker-compose logs -f``

## Sobre

- **Dockerfile**: Define a imagem base, define o diretório de trabalho, instala dependências e copia os arquivos necessários. Também define o comando para iniciar o servidor Uvicorn.
- **docker-compose.yml**: Define dois serviços: web para a aplicação FastAPI e nginx para o servidor Nginx. Configura volumes para montar o código da aplicação e o arquivo de configuração do Nginx.
- **nginx.conf**: Configura o Nginx para usar um bloco upstream que aponta para o serviço web (a aplicação FastAPI), e define uma configuração básica para proxy_pass.
  Com essa estrutura, a aplicação FastAPI e o servidor Nginx são orquestrados pelo Docker Compose, garantindo que estejam configurados e funcionais em um ambiente de container.
