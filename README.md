## Motivação
Aplicação completa para gerenciar seus Todo: adicionar,deletar é atualizar. Existe tambem opção de papeis como admin é usuario comun


## Configuração
- Para utilizar precisa carregar suas configurações do banco
- O arquivo .env_example possuem as variaveis necessarias

  


## Features
- Aprendi trabalhar com autenticação usando JWT
- O pacote exige o caminho do endpoint que sera usado para retornar  o token
- A url ***auth/token**** é endpoint abaixo existe um prefix auth nesse arquivo

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

- Aprendi a usar injeção dependencia , normalmente vamos utilizar  quando alguma funcionalidade é dependente de outra para funcionar

```python

#muitos endpoints dependem do database é user para funcionar

depends_database = Annotated[Session, Depends(get_database)]
depends_user = Annotated[dict, Depends(get_current_user)]



```

##
- Utilizei o alembic para fazer as migrations
- Se preciso de pegar as variaveis do .env é utilizar no arquivo **alembic.ini** preciso utilizar o arquivo env que e fornecido pelo alembic
- Normalmente deixamos o fileConfig sem o if identado totalmente no canto esquerdo
- Nossas entitades precisam estar no target_metada para conseguir criar as tabelas

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
- Exsite um arquivo requirements
- Precisa instalar as dependências necessárias que o projeto exige
- Pode utilizar o comando ***pip ou pip3 install -r requirements.txt***
- Após isto, todas as dependências do projeto estarão instaladas e poderá iniciar o projeto usando o uvicorn 




