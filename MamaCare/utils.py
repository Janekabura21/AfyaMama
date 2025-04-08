def get_parent_phones(immunization):
    # Get the mother's phone number from MaternalProfile
    mother_phone = immunization.child.maternalprofile.telephone
    # Get the father's phone number from ChildProfile
    father_phone = immunization.child.fathers_phone
    return mother_phone, father_phone
