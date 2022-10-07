def user_directory_path(instance):
    return 'user_{0}/'.format(instance.author.id)
