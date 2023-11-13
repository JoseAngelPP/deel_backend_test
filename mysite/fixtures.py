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
