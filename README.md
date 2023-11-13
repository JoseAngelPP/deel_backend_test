# backend-project-template

## Fixtures
To tests the endpoint run the code bellow to create data
```python
# Create companies
from mysite.directory.models import Company, User


company_1, _ = Company.objects.get_or_create(name="Test Company")
company_2, _ = Company.objects.get_or_create(name="Test Company 2")

# Create new users
for i in range(6):
    company_id = 1
    if i % 2 == 0:
        company_id = 2

    company = Company.objects.get(id=company_id)
    user = User.objects.create_user(
        username=f"User {i}",
        first_name="Name",
        last_name="LastName",
        company=company,
        reports_to=User.objects.last()
    )
```

## Welcome
Hello! Welcome to the backend engineering task as part of your interview process with Deel as a Python/Django developer! This task should take about 1-3 hours of your time. As you're completing the tasks below, make sure you document your process including any snags you hit, trade-offs you made, or shortcuts you decided to take. Your decision-making process is equally as important as the completion of these tasks.

### Requirements
- Docker

### Set-up Instructions
This project is already fully configured to launch. You will only need to add data to the DB to get started.

Clone this repository, navigate into the root directory, and boot up using `docker-compose up directory`. This command will pull the base python image, install requirements, migrate and launch the local server.

To add some data, open another shell and connect to the running container with `docker-compose exec directory bash`. You can then navigate into the directory `cd mysite`, and launch the shell with `./manage.py shell`.

### Data & Models
The models in this app are very simple. There are only 3 you need to worry about:
1) The `User` model. This model contains basic attributes from Django, with only the addition of `Company` and `reports_to` foreign keys.
2) The `Company` model. All `User`s have a `Company`. It is a natural grouping for a Enterprise SaaS product.
3) The `Token` object (`from rest_framework.authtoken.models import Token`). This will be used for authenticating a `User` over the API.

To add some data, you can use `create_user`.
```python
>>> from directory.models import *
>>> company = Company.objects.create(name="Test Company")  # Create a new Company
>>> user = User.objects.create_user(username=..., first_name=..., last_name=..., company=company)  # Add a user to the Company.
>>> from rest_framework.authtoken.models import Token  # Import the Token model
>>> token = Token.objects.create(user=user)  # Create an API Token for this new user.
>>> print(token.key)  # Display the API key for this User.
```

You will likely need to add more data to the DB to properly implement the requirements for the tasks below. Creating a script would *probably* be useful. :wink:

### Tasks
1) Make sure that for the `/users` endpoint, that only users for the calling user's company are shown.
2) Update the `reports` action in `UsersViewSet` to return all reports _down_ the reporting tree, recursively.
3) Add another action, similar to `reports`, called `managers`, that does the inverse of `reports`. It should return all users _up_ the reporting tree from the designated user.
4) Add a [filter](https://django-filter.readthedocs.io/en/stable/guide/usage.html#the-filter) for the `/users` endpoint that returns only users that have at least 1 person reporting to them (AKA, filter out users who are/are not managers). Name this filter `is_manager`. It should handle both `true`/`false` values.
5) Add another filter for the `/users` endpoint that returns only users that _do not_ have a manager. Name this filter `has_manager`. It should handle both `true`/`false` values.
6) Update the `/users` endpoint so that for every user in the response, there's a new attribute `num_reports` that is an integer representing the number of users that report to them.
7) Update the `/users` endpoint so that for every user in the response, there's a new attribute `is_isolated` that is a boolean that is `true` if the user has no manager and 0 direct reports. Otherwise it is `false`
8) Add tests. A `mysite/directory/tests/tests.py` file is configured for you. Add tests there. To run the tests, open a second shell and use the `docker-compose exec directory bash` command to enter the running container. Then run the tests with `./manage.py test -v 2`.

### Follow-up Questions
1) Why did you decide to organize the new functions/improvements the way you did? If given more time, how might it be better organized?
I organized the new functionalities in the user serializer by creating two new fields, "managers" and "reports," both of type user. For "reports," I chose to use an array since multiple people can report to the same manager. For "managers," I opted for a single user object since a user typically has only one manager.

- Given more time, I would consider creating separate serializers for "managers" and "reports." Each serializer would have fields like "current_manager" and "all_reports" respectively. Additionally, I would introduce a new field, "levels," as an integer to represent the user's position in the hierarchy. This organization would provide a clearer structure and make it easier to manage the complexity of the user relationships.

2) Provide a few bullet points of optimizations or improvements you would make if given more time.

- Implement caching: Adding caching can significantly improve query times, especially as the dataset grows. However, it's essential to collaborate with the product team to ensure it aligns with the user experience and doesn't introduce any undesirable side effects.
Database Query Optimization: Evaluate and fine-tune database queries for improved efficiency, such as indexing relevant columns or rewriting complex queries.

- Index Usage: Ensure that columns used in frequent queries are appropriately indexed to speed up data retrieval.

- Efficient Pagination: Implement result pagination to avoid unnecessary loading of large datasets and enhance response speed.

- Security: Review and enhance security measures, including input data validation, protection against injection attacks, and adherence to security best practices.

3) Are there any cool features that could be added with minimal effort?
- Search Functionality: Implement a simple search feature to allow users to search for other users.


- CUD (Create, Update, Delete) for users and companies.


Good luck!
