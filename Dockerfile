# O que eu quero puxar 
FROM python:3.12
# O que eu quero rodar 
RUN pip install poetry
# O que eu quero rodar
COPY . /scr
# Muda para a pasta
WORKDIR /scr
RUN poetry install
# Abre essa porta
EXPOSE 8501
# Roda esse comando no seu terminal
ENTRYPOINT ["poetry","run","streamlit","run","app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# COPY ./scr: "Copia tudo que esta presente no meu diretorio do Dockfile para uma imagem do Docker, e com todos os comandos que foram executados á cima"














