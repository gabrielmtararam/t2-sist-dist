1. Executando o Projeto

Passo 1: Utilize docker-compose up para subir o ambiente Docker.

Um exemplo utilizando ubuntu é pelo terminal acessar a pasta do projeto e executar:
`sudo docker-compose up --build`

Caso queira, antes de executar o comando up, execute o comando abaixo para se certificar que não existe 
outro container similar sendo executado
`docker-compose down`


Passo 2: Acesse o terminal do contêiner Python `(docker exec -it <nome_do_container_python_app> /bin/sh`) e execute python main.py para iniciar a simulação manual.

Um exemplo, seria inicialmente listar os containers disponíveis, com o comando, em um terminal diferente da primeira etapa,
`docker ps -a`  para obter o id do container desejado.
Em seguida executar o comando `docker exec -it 016d28e75df5 /bin/sh` porém substituindo "016d28e75df5" pelo id do container
por fim, executar `python ./main.py`

Configurando acesso a base de dados

com `docker ps -a` encontre o id do container do redis

Descubra o ip deste container com 
 `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 277e4956474c`
substitindo 277e4956474c pelo id do container redis

Atualize o código python para o ip do redis