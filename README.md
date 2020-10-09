# django-vpn-gateway-administrator-app
Test task that tracks the company's traffic limit

# Access
Admin panel
Login: admin
Password: admin_password_1234

# for run local
## Import dump

```bash
gunzip django-vpn-gateway-administrator-app.sql.gz
mysql -u root -p < django-vpn-gateway-administrator-app
## Create user

*under mysql root user, change <PASSWORD>*

```sql
CREATE USER '<USER>'@'localhost' IDENTIFIED BY '<PASSWORD>';
GRANT ALL PRIVILEGES ON vpn_admin.* TO '<USER>'@'localhost';
```

## Django settings

*`vpn_admin/settings.py`, change <PASSWORD>*

```python
...
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vpn_admin',
            'USER': '<USER>',
            'PASSWORD': '<PASSWORD>',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
...
```

## Change site admin password

```bash
python3 manage.py changepassword admin
```
pip3 install requirements.txt
python3 manage.py runserver
