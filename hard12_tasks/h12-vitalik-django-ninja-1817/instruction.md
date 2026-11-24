You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

all fields of response become None after sending it

Hi, I'm not good in English.

We are implementing a website for doctors and in a specific endpoint, we want to send work shifts in a specific structure.

I'm the person who implement the APIs and I wrote the logic of that endpoint, data correctly generated but when returning the response to client, all fields become None|null.

here is schemas:
```python
class WorkShiftSchema(Schema):
    start_hour: Optional[str] = None
    end_hour: Optional[str] = None
    start_minute: Optional[str] = None
    end_minute: Optional[str] = None

class WorkDaysDetailSchema(Schema):
    f0: WorkShiftSchema = Field(None, alias="0")
    f1: WorkShiftSchema = Field(None, alias="1")

    class Config(Schema.Config):
        populate_by_name = True

class WorkDaysSchema(Schema):
    f0: WorkDaysDetailSchema = Field(None, alias="0")
    f1: WorkDaysDetailSchema = Field(None, alias="1")
    f2: WorkDaysDetailSchema = Field(None, alias="2")
    f3: WorkDaysDetailSchema = Field(None, alias="3")
    f4: WorkDaysDetailSchema = Field(None, alias="4")
    f5: WorkDaysDetailSchema = Field(None, alias="5")
    f6: WorkDaysDetailSchema = Field(None, alias="6")

    class Config(Schema.Config):
        populate_by_name = True

class WorkDaysResponse(Schema):
    data: WorkDaysSchema
    errors: None
```

here is data generator:
```python
def get_time_from_slot(slot, field):
    response_hour = slot[f'{field}_hour']
    response_minute = slot[f'{field}_minute']
    response = ':'.join([response_hour, response_minute])
    return response

def get_doctor_work_days(doctor):
    days_list = doctor.workshift.work_days
    values = schema.WorkDaysSchema()

    day_mapping = {
        '0': 'f0',
        '1': 'f1',
        '2': 'f2',
        '3': 'f3',
        '4': 'f4',
        '5': 'f5',
        '6': 'f6',
    }

    for day_index, data in days_list.items():
        detail = schema.WorkDaysDetailSchema()
        is_active = any(slot for slot in data)
        if is_active:
            for i, slot in data.items():
                if not slot:
                    continue

                start_hour, start_min = get_time_from_slot(slot, 'start').split(':')
                end_hour, end_min = get_time_from_slot(slot, 'end').split(':')


                field = schema.WorkShiftSchema(
                    start_hour=start_hour,
                    end_hour=end_hour,
                    start_minute=start_min,
                    end_minute=end_min,
                )
                setattr(detail, f'f{i}', field)
            setattr(values, day_mapping[day_index], detail)
        else:
            setattr(values, day_mapping[day_index], None)

    response = schema.WorkDaysResponse(
        data=values,
        errors=None
    )
    return response
```

and here is the endpoint:
```python
WORKSHIFT_DETAIL = {
    200: schema.WorkDaysResponse,
    400: schema.Error
}

@router.get('workshift', auth=DoctorJWTAuth(), tags=['doctors'], response=WORKSHIFT_DETAIL, by_alias=True)
def get_workshift(request):
    doctor = request.doctor
    # return doctor.workshift.work_days
    response = schema_gen.get_doctor_work_days(doctor)
    return 200, response
```

the `values` variable contains the correct data, but response of this endpoint is like this:
```
{
  "data": {
    "0": {
      "0": {
        "start_hour": null,
        "end_hour": null,
        "start_minute": null,
        "end_minute": null
      },
      "1": {
        "start_hour": null,
        "end_hour": null,
        "start_minute": null,
        "end_minute": null
      }
    },
    "1": {
    ...
    }
  },
  "errors": null
}
```

I changed some codes when writing here, variable names may have some mismatch.
