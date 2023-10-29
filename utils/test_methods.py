from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import DataError, IntegrityError


def create_test_instance(values, model, with_manager=True):
    errors = []
    try:
        with transaction.atomic():
            instance = model.objects.create(**values)
            instance.full_clean()
    except (
        ValidationError,
        DataError,
        IntegrityError,
        ValueError,
        TypeError,
    ) as e:
        errors = [arg for arg in e.args if arg is not None]
        instance = None
    if errors:
        return instance, errors
    return instance, None


def bulk_create_test_instances(values, model, has_constraints=False):
    success_list = []
    error_list = []
    eval_dict = {}
    for item in values:
        eval_dict.update(item[0])
        instance, errors = create_test_instance(
            values=eval_dict, model=model
        )
        if item[1]:
            instance_check = isinstance(instance, model)
            success_list.append(instance_check)
            if not instance_check:
                error_list.append([item, errors])
        else:
            instance_check = instance is None
            success_list.append(instance_check)
            if not instance_check:
                error_list.append([item, "Was wrongfully created."])
        if has_constraints and instance is not None:
            instance.delete()
    return success_list, error_list
