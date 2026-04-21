allowed_path = ['/', '/login/', '/auth/google/', '/accounts/login/', '/accounts/logout/', '/accounts/signup/']
path = "/"

print(not any(url.startswith(path) for url in allowed_path))