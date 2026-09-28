from django.db import migrations, models
import django.db.models.deletion


def copy_career_skills(apps, schema_editor):
    Career = apps.get_model('careers', 'Career')
    CareerSkill = apps.get_model('careers', 'CareerSkill')

    through_model = Career.skills.through

    existing_relationships = through_model.objects.all()

    for relationship in existing_relationships:

        CareerSkill.objects.get_or_create(
            career_id=relationship.career_id,
            skill_id=relationship.skill_id
        )


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0002_alter_category_options'),
    ]

    operations = [

        # --------------------------------
        # 1. Create CareerSkill table
        # --------------------------------

        migrations.CreateModel(
            name='CareerSkill',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'importance',
                    models.CharField(
                        choices=[
                            ('LOW', 'Low'),
                            ('MEDIUM', 'Medium'),
                            ('HIGH', 'High'),
                            ('CRITICAL', 'Critical'),
                        ],
                        default='MEDIUM',
                        max_length=20
                    )
                ),
                (
                    'target_proficiency',
                    models.DecimalField(
                        decimal_places=2,
                        default=70.0,
                        max_digits=5
                    )
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True
                    )
                ),
                (
                    'career',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='career_skills',
                        to='careers.career'
                    )
                ),
                (
                    'skill',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='career_skills',
                        to='careers.skill'
                    )
                ),
            ],
        ),

        # --------------------------------
        # 2. Copy old relationships
        # --------------------------------

        migrations.RunPython(
            copy_career_skills,
            migrations.RunPython.noop
        ),

        # --------------------------------
        # 3. Remove old ManyToMany field
        # --------------------------------

        migrations.RemoveField(
            model_name='career',
            name='skills',
        ),

        # --------------------------------
        # 4. Add new ManyToMany field
        # --------------------------------

        migrations.AddField(
            model_name='career',
            name='skills',
            field=models.ManyToManyField(
                blank=True,
                related_name='careers',
                through='careers.CareerSkill',
                to='careers.skill',
            ),
        ),

        # --------------------------------
        # 5. Prevent duplicate relationships
        # --------------------------------

        migrations.AddConstraint(
            model_name='careerskill',
            constraint=models.UniqueConstraint(
                fields=('career', 'skill'),
                name='unique_career_skill'
            ),
        ),
    ]