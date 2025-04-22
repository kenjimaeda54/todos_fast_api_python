## Motivação
Aplicação completa para gerenciar suas tarefas: adicionar, deletar e atualizar. Existe também opção de papéis como admin é usuário comum

## Configuração
- Para utilizar, precisa carregar suas configurações do banco.
- O arquivo .env_example possui as variáveis necessárias

  


## Features
- Aprendi a trabalhar com autenticação usando JWT
- O pacote exige o caminho do endpoint que será usado para retornar o token.
- A url ***auth/token**** é endpoint, existe um prefix auth nessa url.

```python
oauth_depends = OAuth2PasswordBearer(tokenUrl='auth/token')


@router.post("/token",response_model=TokenResponse)
async  def  read_token_authenticated(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db: depends_db):
       user_database = return_user_if_authenticated(form_data.username,form_data.password,db)

       if user_database is None:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not unauthorized")

       token =  return_token_jwt(user_database,timedelta(minutes=20))
       return TokenResponse(
          access_token=token,
           token_type="bearer"
       )


```

##

- Aprendi a usar injeção dependência, normalmente vamos utilizar quando alguma funcionalidade é dependente de outra para funcionar.

```python

#muitos endpoints dependem do database é user para funcionar

depends_database = Annotated[Session, Depends(get_database)]
depends_user = Annotated[dict, Depends(get_current_user)]



```

##
- Utilizei o alembic para fazer as migrações.
- Só preciso pegar as variáveis do .env para utilizar no arquivo **alembic.ini** . 
- Não conseguimos importar diretamente no alembic.ini
- Por isso utilizamos o arquivo env fornecido pelo alembic
- Deixamos normalmente o fileConfig sem o if identado totalmente no canto esquerdo.
- Nossas entidades precisam estar no target_metada para conseguir criar as tabelas.


```python

  alembic
  |
  |
  |
   -- env.py 


#env


load_dotenv()

user_password_database  = os.environ.get("PASSWORD")
user_name_database = os.environ.get("USER")
name_database  = os.environ.get("NAME_DATABASE")

alchemy_url_database = f'postgresql://{user_name_database}:{user_password_database}@localhost/{name_database}'



target_metadata = entities.Base.metadata


```

## Como iniciar
- Existe um arquivo requirements.txt
- Após estar na raiz do projeto, crie seu ambiente virtual usando ***python3 -m venv <nomesugestivo>***
- Aplica o source ***source nomesugestivo/bin/activate**
- Precisa instalar as dependências necessárias que o projeto exige.
- Pode utilizar o comando ***pip ou pip3 install -r requirements.txt***
- Após isto, todas as dependências do projeto estarão instaladas e poderá iniciar o projeto usando o uvicorn 



