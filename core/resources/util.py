from core.models.user import UserModel


def validate_users(users):
    for id in users:
        if not UserModel.find_by_id(id):
            raise Exception(f"No user found with {id}")


def get_to_pay_dict_list(obj_list):
    data_list = []
    for itm in obj_list:
        data = {}
        data['paying_user'] = itm.user_to_pay.email
        data['user_getting_paid'] = itm.paying_user.email
        data['amount'] = itm.amount
        data_list.append(data)
    return data_list