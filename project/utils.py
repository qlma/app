
def is_staff(self):
    user_type = self.request.user.get_user_type_display()
    allowed_roles=['Teacher', 'Admin']
    if user_type in allowed_roles:
        return True
    return False

def is_author(self):
    post = self.get_object()
    if self.request.user == post.author:
        return True
    return False