from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200, verbose_name='선택항목')),
                ('votes', models.IntegerField(default=0, verbose_name='투표수')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='질문')),
                ('total_count', models.IntegerField(default=0, verbose_name='전체투표수')),
            ],
        ),
        migrations.CreateModel(
            name='PollList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='제목')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='등록일')),
                ('start_date', models.DateField(default=django.utils.timezone.now, verbose_name='시작일')),
                ('end_date', models.DateField(default=django.utils.timezone.now, verbose_name='종료일')),
                (
                    'status',
                    models.CharField(
                        choices=[('OP', 'Open'), ('CL', 'Closed')],
                        default='OP',
                        max_length=2,
                        verbose_name='상태',
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='poll',
            name='poll_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.polllist'),
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.poll'),
        ),
    ]
