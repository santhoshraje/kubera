def does_user_exist(user_id):
    with open("users.txt", mode="r+") as file:
        lines = [line.rstrip() for line in file.readlines()]

        if user_id in lines:
            return True
        else:
            file.write(f"\n{user_id}")
            return False
