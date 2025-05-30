

# Para rodar
task run





## Gerando imagem
- "A imagem é como se fosse um zip do teu código com o seu computador"
´´´
docker build -t minha-primeira-imagem .
´´´

## Lista imagens
docker images

## Comando que deszipa a imagem
docker run -d -p 8501:8501 --name my-first-container minha-primeira-imagem

REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
minha-primeira-imagem     latest            77d2c49baf05   3 months ago    1.62GB


