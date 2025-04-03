

## Gerando imagem
- "A imagem é como se fosse um zip do teu código com o seu computador"
´´´
docker build -t minha-primeira-imagem .
´´´

## Lista imagens
docker images

## Comando que deszipa a imagem
docker run -d -p 8501:8501 --name my-first-container minha-primeira-imagem









