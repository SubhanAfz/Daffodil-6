# Team Daffodil-6 Small Group project

## Team members
The members of the team are:
- *Muhammad Subhan Afzal*
- *Frederick George Brooke*
- *Mahe Chowdury*
- *Mohamed Ismail Elghuwael*
- *Minhal (Minhal) Valiya Peedikakkal*

## Project structure
The project is called `recipify`.  It currently consists of a single app `recipes`.

## Deployed version of the application
The deployed version of the application can be found at [recipify.subhan.work](http://recipify.subhan.work).

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  The project source code has been developed using Python 3.12, so you are recommended to use the same version.  From the root of the project:

```
$ python3.12 -m venv venv
$ source venv/bin/activate
```

If your system does not have `python3.12` installed and you are unable to install Python 3.12 as a version you can explicitly refer to from the CLI, then replace `python3.12` by `python3` or `python`, provide this employs a relatively recent version of Python.

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

The [dataset](https://github.com/SubhanAfz/Daffodil-6/blob/main/recipes/management/recipes_data_sample_1.csv) the seeder uses comes from here: [source](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images?resource=download&select=Food+Images)

We have used Generative AI to review GitHub Pull Requests. All the Pull Requests which have used Generative AI are shown below:

[#5](https://github.com/SubhanAfz/Daffodil-6/pull/5)
[#6](https://github.com/SubhanAfz/Daffodil-6/pull/6)
[#7](https://github.com/SubhanAfz/Daffodil-6/pull/7)
[#8](https://github.com/SubhanAfz/Daffodil-6/pull/8)
[#10](https://github.com/SubhanAfz/Daffodil-6/pull/10)
[#11](https://github.com/SubhanAfz/Daffodil-6/pull/11)
[#12](https://github.com/SubhanAfz/Daffodil-6/pull/12)
[#14](https://github.com/SubhanAfz/Daffodil-6/pull/14)
[#15](https://github.com/SubhanAfz/Daffodil-6/pull/15)
[#18](https://github.com/SubhanAfz/Daffodil-6/pull/18)
[#19](https://github.com/SubhanAfz/Daffodil-6/pull/19)
[#21](https://github.com/SubhanAfz/Daffodil-6/pull/21)
[#23](https://github.com/SubhanAfz/Daffodil-6/pull/23)