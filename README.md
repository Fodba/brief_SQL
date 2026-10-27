# brief_SQL

## Technique Postgres

Pour qu'un utilisateur puisse accéder a la base Postgres : 
Connecter vous à Postgres : 
```sudo -u postgres psql  ```

```
-- 1. Si l'utilisateur 'joce' n'existe pas encore, créez-le avec un mot de passe :
CREATE USER user_name WITH PASSWORD 'votre_mot_de_passe_securise';

-- OU 2. S'il existe déjà mais n'a pas de mot de passe, définissez-en un :
ALTER USER user_name WITH PASSWORD 'votre_mot_de_passe_securise';

-- 3. Donnez-lui le droit de créer des bases de données (très utile pour votre script) :
ALTER USER user_name CREATEDB;

-- 4. Donnez-lui l'accès à la base de données 'postgres' par défaut :
GRANT CONNECT ON DATABASE postgres TO user_name;
```

Verifier les mode de connection de postgres
```
sudo vim pg_hba.conf
```

Modifier peer par scram-sha-256