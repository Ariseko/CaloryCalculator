async def calc(gender, activity, age, weight, height):
    if gender == "male":
        baseMetabolismMale = (9.99 * weight) + (6.25 * height) - (4.92 * age) + 5
        calloryMale = baseMetabolismMale * activity

        return calloryMale

    elif gender == "female":
        baseMetabolismFemale = (9.99 * weight) + (6.25 * height) - (4.92 * age) - 161
        calloryFemale = baseMetabolismFemale * activity

        return calloryFemale
