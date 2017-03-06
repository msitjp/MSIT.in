# MSIT Website
###### Testing Branch

### Follow these steps to setup the project locally
```sh
$ git clone https://www.github.com/htadg/MSIT.in msit
$ cd msit
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

If you want to work on the current testing branch
```sh
$ git checkout testing
# Make Upgrades to the Project
$ git add --add
$ git commit -m "Fixed :: Something that was really Bad ;)"
$ git push origin testing
```
After these steps the project should be up at [http://localhost:8000/](http://localhost:8000/)

Now you can access the Admin Panel through [http://localhost:8000/admin](http://localhost:8000/admin) and login with your newly created username and password.
