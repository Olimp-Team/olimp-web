from users.models import User


def create_users():
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'icw20@mail.ru',
            'first_name': 'Jony',
            'last_name': 'Ivanitsky',
            'is_staff': True,
            'is_superuser': True,
            'is_admin': True,
            'password': '732301papa'
        }
    )
    if created:
        admin_user.set_password('732301papa')
        admin_user.save()
        print("Admin создан")

    teacher_user, created = User.objects.get_or_create(
        username='teacher',
        defaults={
            'email': 'icw20@mail.ru',
            'first_name': 'Georg',
            'last_name': 'Muller',
            'is_teacher': True,
            'password': '732301papa'
        }
    )
    if created:
        teacher_user.set_password('732301papa')
        teacher_user.save()
        print('teacher создан')

    student_user, created = User.objects.get_or_create(
        username='student',
        defaults={
            'email': 'icw20@mail.ru',
            'first_name': 'Charlotte',
            'last_name': 'Rici',
            'is_child': True,
            'password': '732301papa'
        }
    )
    if created:
        student_user.set_password('732301papa')
        student_user.save()
        print('Student создан')


create_users()
